"""
Management command: extract_api_urls

Given an app name, this command:
  1. Looks at the project's ROOT_URLCONF (e.g. conf/urls.py) to find the
     path(..., include('<app>.urls')) entry and grabs its URL prefix.
  2. Walks <app>/urls.py to find every path()/re_path() entry.
  3. For each entry, resolves the view class (works for plain Django class
     based views, DRF APIView/generic views, and DRF viewsets registered
     via .as_view({...})) and figures out which HTTP methods it supports.
  4. Builds a JSON array of {"method": ..., "url": ...} objects, with Django
     path converters like <uuid:contractid> normalised to {contractid}.
  5. Cross-checks every (method, url) pair against the `Apis` model
     (looked up by class name across all installed apps, so it doesn't
     matter which app it lives in). If a matching row exists, its `desc`
     is used as-is (even if blank). If no row exists, `desc` is set to
     the literal string defined in NOT_AVAILABLE_DESC below.

Usage:
    python manage.py extract_api_urls contracts
    python manage.py extract_api_urls contracts --output contracts_endpoints.json
    python manage.py extract_api_urls contracts --skip-db-check
"""
import json
import re

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver

# Only "real" HTTP verbs - skip head/options/trace, which are handled
# generically by almost every View and aren't interesting here.
HTTP_METHODS = ["get", "post", "put", "patch", "delete"]

# Exact string used for `desc` when no (method, url) row exists in the Apis
# table. Change this in one place if you need a different literal value.
NOT_AVAILABLE_DESC = "NOT AVAILABLE"


def get_route_string(pattern):
    """
    Return the raw route string for a URLPattern/URLResolver's `.pattern`.
    Handles both path() (RoutePattern, has `._route`) and re_path()
    (RegexPattern, only has `.regex.pattern`) definitions.
    """
    if hasattr(pattern, "_route"):
        return pattern._route
    return pattern.regex.pattern


def normalize_placeholders(route):
    """
    Convert Django's path-converter / regex-group syntax into plain
    {name} placeholders.

        <uuid:contractid>        -> {contractid}
        <int:shrhbaseid>         -> {shrhbaseid}
        <contractid>             -> {contractid}
        (?P<contractid>[0-9a-f-]+)  -> {contractid}   (re_path case)
    """
    # Must run BEFORE the <converter:name> substitution below - otherwise
    # that regex partially matches the "<name>" inside "(?P<name>...)" and
    # leaves a mangled "(?P{name}...)" behind.
    route = re.sub(r"\(\?P<([^>]+)>[^)]*\)", r"{\1}", route)
    route = re.sub(r"<(?:[^:>]+:)?([^>]+)>", r"{\1}", route)
    route = route.replace("^", "").replace("$", "")
    return route


def join_url_parts(*parts):
    cleaned = [p.strip("/") for p in parts if p and p.strip("/")]
    return "/".join(cleaned)


def clean_url(url):
    url = "/" + url.strip("/") + "/"
    return re.sub(r"/{2,}", "/", url)


def get_view_class(callback):
    """
    Recover the view class from a resolved URL callback.
    - Plain Django CBVs: View.as_view() sets `callback.view_class`.
    - DRF APIView subclasses: DRF additionally sets `callback.cls`
      (and still carries `view_class` through, since APIView.as_view()
      wraps Django's View.as_view() with csrf_exempt(), which copies
      the underlying function's __dict__).
    """
    return getattr(callback, "cls", None) or getattr(callback, "view_class", None)


def get_methods(callback, view_class):
    if view_class is not None:
        methods = [m.upper() for m in HTTP_METHODS if hasattr(view_class, m)]
        if methods:
            return methods
    # DRF ViewSets bound via SomeViewSet.as_view({'get': 'list', 'post': 'create'})
    actions = getattr(callback, "actions", None)
    if actions:
        return sorted(m.upper() for m in actions.keys())
    # Function-based view - we can't introspect verbs, assume GET.
    return ["GET"]


class Command(BaseCommand):
    help = (
        "Extract a JSON list of {method, url} entries for every endpoint "
        "in <app_name>/urls.py, using the prefix that app is mounted under "
        "in the root URLconf."
    )

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str, help="e.g. 'contracts'")
        parser.add_argument(
            "--output",
            "-o",
            type=str,
            default=None,
            help="Optional file path to write the JSON output to.",
        )
        parser.add_argument(
            "--skip-db-check",
            action="store_true",
            default=False,
            help="Skip the Apis-table lookup and omit 'desc' from the output.",
        )

    def handle(self, *args, **options):
        app_name = options["app_name"]
        output_path = options.get("output")

        root_resolver = get_resolver()
        prefix, app_url_patterns = self.find_app_include(root_resolver, app_name)

        if prefix is None:
            raise CommandError(
                f"Could not find include('{app_name}.urls') anywhere in the "
                f"root URLconf. Make sure '{app_name}' is mounted with "
                f"path('...', include('{app_name}.urls'))."
            )

        self.stdout.write(
            self.style.SUCCESS(f"Found '{app_name}' mounted at prefix: /{prefix.strip('/')}/")
        )

        endpoints = self.walk_patterns(app_url_patterns, base_prefix=prefix)

        self.stdout.write(self.style.SUCCESS(f"Extracted {len(endpoints)} endpoint entries."))

        if not options["skip_db_check"]:
            endpoints = self.attach_descriptions(endpoints)
            self.stdout.write(self.style.SUCCESS("Cross-checked endpoints against the Apis table."))

        output_json = json.dumps(endpoints, indent=2, ensure_ascii=False)

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(output_json)
            self.stdout.write(self.style.SUCCESS(f"Written to {output_path}"))
        else:
            self.stdout.write(output_json)

    def find_app_include(self, resolver, app_name):
        """
        Search the root resolver's top-level url_patterns for the
        URLResolver produced by include('<app_name>.urls'), and return
        (prefix_string, its_url_patterns).
        """
        target = f"{app_name}.urls"
        for entry in resolver.url_patterns:
            if isinstance(entry, URLResolver):
                module = entry.urlconf_module
                module_name = getattr(module, "__name__", None)
                if module_name == target:
                    prefix = get_route_string(entry.pattern)
                    return prefix, entry.url_patterns
        return None, None

    def walk_patterns(self, url_patterns, base_prefix, nested_prefix=""):
        """
        Recursively walk a list of URLPattern/URLResolver objects (handles
        the case where the app's own urls.py has further include() calls),
        returning a flat list of {"method", "url"} dicts.
        """
        endpoints = []
        for entry in url_patterns:
            if isinstance(entry, URLPattern):
                route = get_route_string(entry.pattern)
                full_route = join_url_parts(base_prefix, nested_prefix, route)
                url = clean_url(normalize_placeholders(full_route))

                view_class = get_view_class(entry.callback)
                methods = get_methods(entry.callback, view_class)

                for method in methods:
                    endpoints.append({"method": method, "url": url})

            elif isinstance(entry, URLResolver):
                deeper_prefix = get_route_string(entry.pattern)
                endpoints.extend(
                    self.walk_patterns(
                        entry.url_patterns,
                        base_prefix,
                        nested_prefix + "/" + deeper_prefix,
                    )
                )
        return endpoints

    def get_apis_model(self):
        """
        Locate the `Apis` model by class name, regardless of which app it
        lives in, so this command doesn't need to hard-code an import path.
        """
        matches = [m for m in apps.get_models() if m.__name__ == "Apis"]
        if not matches:
            raise CommandError(
                "Could not find a model named 'Apis' in any installed app. "
                "Make sure the app containing it is listed in INSTALLED_APPS, "
                "or pass --skip-db-check to skip this step."
            )
        if len(matches) > 1:
            labels = ", ".join(f"{m._meta.app_label}.{m.__name__}" for m in matches)
            raise CommandError(
                f"Found more than one model named 'Apis': {labels}. "
                "This command only supports a single Apis model."
            )
        return matches[0]

    def attach_descriptions(self, endpoints):
        """
        For every {"method", "url"} entry, look up the matching row in the
        Apis table (unique on method+url) and add a "desc" key:
          - row exists  -> desc is copied from the DB as-is (even if blank)
          - no row      -> desc is set to NOT_AVAILABLE_DESC
        """
        if not endpoints:
            return endpoints

        Apis = self.get_apis_model()

        lookup = Q()
        for e in endpoints:
            lookup |= Q(method=e["method"], url=e["url"])

        existing = {
            (rec.method, rec.url): rec.desc
            for rec in Apis.objects.filter(lookup)
        }

        for e in endpoints:
            key = (e["method"], e["url"])
            e["desc"] = existing[key] if key in existing else NOT_AVAILABLE_DESC

        return endpoints