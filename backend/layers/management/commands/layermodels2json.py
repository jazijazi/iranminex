import json

from django.apps import apps
from django.core.management.base import BaseCommand

# Adjust this import to match your actual project layout if it differs.
from layers.models.models import LinkedToLayerTable


def safe_value(value):
    """Return a JSON-serializable version of `value`, falling back to str()."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (list, tuple)):
        return [safe_value(v) for v in value]
    if isinstance(value, dict):
        return {str(k): safe_value(v) for k, v in value.items()}
    try:
        json.dumps(value)
        return value
    except (TypeError, ValueError):
        return str(value)


def get_default(field):
    """Resolve a field's default, turning callables into a readable marker."""
    if not field.has_default():
        return None
    default = field.default
    if callable(default):
        name = getattr(default, "__name__", None)
        return f"<callable:{name or str(default)}>"
    return safe_value(field.get_default())


def get_choices(field):
    """Normalize field.choices (including grouped choices) into plain JSON."""
    if not field.choices:
        return None
    result = []
    for value, label in field.choices:
        if isinstance(label, (list, tuple)):  # grouped choices
            group = [[safe_value(v), str(l)] for v, l in label]
            result.append([safe_value(value), group])
        else:
            result.append([safe_value(value), str(label)])
    return result


def field_to_dict(field):
    """Build a JSON-serializable dict describing a single model field."""
    data = {
        "name": field.name,
        "attname": getattr(field, "attname", field.name),
        "type": type(field).__name__,
        "internal_type": field.get_internal_type() if hasattr(field, "get_internal_type") else None,
        "verbose_name": str(getattr(field, "verbose_name", field.name)),
        "help_text": str(getattr(field, "help_text", "")) or None,
        "null": getattr(field, "null", None),
        "blank": getattr(field, "blank", None),
        "unique": getattr(field, "unique", None),
        "primary_key": getattr(field, "primary_key", None),
        "editable": getattr(field, "editable", None),
        "db_column": getattr(field, "db_column", None),
        "db_index": getattr(field, "db_index", None),
        "default": get_default(field),
        "choices": get_choices(field),
    }

    # CharField / SlugField / etc.
    if getattr(field, "max_length", None) is not None:
        data["max_length"] = field.max_length

    # DecimalField
    if getattr(field, "max_digits", None) is not None:
        data["max_digits"] = field.max_digits
    if getattr(field, "decimal_places", None) is not None:
        data["decimal_places"] = field.decimal_places

    # Date / DateTime auto flags
    if hasattr(field, "auto_now"):
        data["auto_now"] = field.auto_now
    if hasattr(field, "auto_now_add"):
        data["auto_now_add"] = field.auto_now_add

    # GeoDjango fields (PointField, MultiPolygonField, MultiLineStringField, ...)
    if hasattr(field, "srid"):
        data["srid"] = field.srid
        data["geom_type"] = getattr(field, "geom_type", None)
        data["dim"] = getattr(field, "dim", None)
        data["geography"] = getattr(field, "geography", None)
        data["spatial_index"] = getattr(field, "spatial_index", None)

    # Relational fields (ForeignKey, OneToOneField, ManyToManyField)
    if getattr(field, "is_relation", False):
        related_model = field.related_model
        data["related_model"] = (
            f"{related_model._meta.app_label}.{related_model.__name__}"
            if related_model else None
        )
        remote_field = getattr(field, "remote_field", None)
        on_delete = getattr(remote_field, "on_delete", None)
        if on_delete:
            data["on_delete"] = getattr(on_delete, "__name__", str(on_delete))
        related_name = getattr(remote_field, "related_name", None)
        if related_name:
            data["related_name"] = related_name
        data["many_to_many"] = field.many_to_many
        data["many_to_one"] = field.many_to_one
        data["one_to_many"] = field.one_to_many
        data["one_to_one"] = field.one_to_one

    return data


class Command(BaseCommand):
    help = (
        "Export every concrete model inheriting from LinkedToLayerTable "
        "to a JSON description of its fields."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--indent",
            type=int,
            default=2,
            help="JSON indent level (default: 2). Use 0 for compact single-line output.",
        )
        parser.add_argument(
            "--output",
            type=str,
            default=None,
            help="Write JSON to this file path instead of printing to stdout.",
        )

    def handle(self, *args, **options):
        indent = options["indent"] or None
        if indent == 0:
            indent = None

        models_data = []

        for model in apps.get_models():
            if model is LinkedToLayerTable:
                continue
            if model._meta.abstract:
                continue
            if not issubclass(model, LinkedToLayerTable):
                continue

            fields = list(model._meta.fields) + list(model._meta.many_to_many)

            models_data.append({
                "class_name": model.__name__,
                "app_label": model._meta.app_label,
                "db_table": model._meta.db_table,
                "verbose_name": str(model._meta.verbose_name),
                "verbose_name_plural": str(model._meta.verbose_name_plural),
                "module": model.__module__,
                "fields": [field_to_dict(f) for f in fields],
            })

        models_data.sort(key=lambda m: m["class_name"])

        output_json = json.dumps(models_data, indent=indent, ensure_ascii=False)

        if options["output"]:
            with open(options["output"], "w", encoding="utf-8") as f:
                f.write(output_json)
            self.stderr.write(self.style.SUCCESS(
                f"Wrote {len(models_data)} model(s) to {options['output']}"
            ))
        else:
            self.stdout.write(output_json)