"""

Part 1 - generic filtering helpers shared by every app (BaseFilterSet and the
typed filters). Nothing in part 1 knows about a specific app or model, so it
must never import from other apps.
Part 2 - FilterSets for this app's own models (Ostan, Shahrestan, Pelak).

Use ``BaseFilterSet`` as the parent of every new FilterSet. It reads
``Meta.model`` and builds the filters for every concrete field by itself, so a
normal FilterSet is just:

    from common.filters import BaseFilterSet

    class ContractFilterSet(BaseFilterSet):
        class Meta:
            model = Contract

URL parameters generated per field type
------------------------------------------------------------------------------
CharField / TextField      ?title=road                  contains, ignore case
                           ?title__exact=Road 1         exact match
field with choices         ?status=draft                exact (validated)
                           ?status__in=draft,returned   any of
ForeignKey / OneToOne      ?shahrestan=5                by id
                           ?shahrestan__in=5,6          any of
Integer / Float / Decimal  ?masahat=10                  exact
                           ?masahat_min=5&masahat_max=20
DateField                  ?date=2026-01-01             exact
                           ?date_from=...&date_to=...   inclusive range
DateTimeField              ?created_from=...&created_to=...   by calendar day
                           (created_at -> created_*, updated_at -> updated_*)
BooleanField               ?flag=true
ManyToManyField            ?typ=1,2,3                   linked to ANY of these ids
primary key                ?id=5    ?id__in=5,6,7
nullable field (any type)  ?karbargone__isnull=true     (or false)
every model                ?ordering=-created_at,title  ("-" = descending)

Not generated automatically: FileField, geometry, JSON and reverse relations
(for those only ``__isnull`` is generated, when the column is nullable).
Declare the rest by hand on the FilterSet. A filter you declare yourself always
wins over the generated one with the same name.

Meta options (all optional)
    exclude_fields = ("some_field",)   # skip these model fields entirely
"""
from collections import OrderedDict

import django_filters as df
from django import forms
from django.db import models
from django_filters.constants import EMPTY_VALUES
from django_filters.widgets import BooleanWidget


__all__ = [
    "BaseFilterSet",
    "IntegerFilter",
    "IntegerInFilter",
    "CharInFilter",
    "StableOrderingFilter",
]


# ---------------------------------------------------------------------------
# Small typed filters
# ---------------------------------------------------------------------------

class IntegerFilter(df.NumberFilter):
    """Whole numbers only: ?shahrestan=abc and ?shahrestan=1.5 fail validation."""
    field_class = forms.IntegerField


class IntegerInFilter(df.BaseInFilter, IntegerFilter):
    """?field=1,2,3 (every item validated as an integer)."""


class CharInFilter(df.BaseInFilter, df.CharFilter):
    """?field=a,b,c"""


class StableOrderingFilter(df.OrderingFilter):
    """
    OrderingFilter that always adds the primary key as the last sort key.
    Sorting by a non-unique column (status, shahrestan, ...) would otherwise
    let rows move between pages when paginating.
    """

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        ordering = [self.get_ordering_value(param) for param in value]
        ordering.append("pk")  # repeated keys are dropped by Django
        return qs.order_by(*ordering)


# ---------------------------------------------------------------------------
# Field -> filters mapping
# ---------------------------------------------------------------------------

def _filters_for_field(field):
    """
    Return ``(filters, order_column)`` for one model field.

    ``filters`` maps URL parameter name -> Filter. ``order_column`` is the
    column ``?ordering=<field name>`` sorts by (None = not sortable).
    """
    name = field.name
    out = OrderedDict()
    order_column = None

    if field.many_to_many:
        # ?typ=1,2,3 -> rows linked to ANY of these ids. The join can repeat
        # rows, so the filter de-duplicates by itself.
        out[name] = IntegerInFilter(field_name=f"{name}__id", distinct=True)
        return out, None

    if field.is_relation:  # ForeignKey / OneToOneField: filter on the raw id column
        column = field.attname  # e.g. shahrestan_id
        out[name] = IntegerFilter(field_name=column)
        out[f"{name}__in"] = IntegerInFilter(field_name=column)
        order_column = column

    elif field.choices:
        out[name] = df.ChoiceFilter(field_name=name, choices=list(field.flatchoices))
        out[f"{name}__in"] = CharInFilter(field_name=name)
        order_column = name

    elif isinstance(field, models.BooleanField):
        out[name] = df.BooleanFilter(field_name=name, widget=BooleanWidget())
        order_column = name

    elif isinstance(field, models.DateTimeField):  # before DateField: it is a subclass
        stem = name[:-3] if name.endswith("_at") else name  # created_at -> created
        # `date__` compares calendar days, so created_to=2026-01-31 includes the whole 31st
        out[f"{stem}_from"] = df.DateFilter(field_name=name, lookup_expr="date__gte")
        out[f"{stem}_to"] = df.DateFilter(field_name=name, lookup_expr="date__lte")
        order_column = name

    elif isinstance(field, models.DateField):
        out[name] = df.DateFilter(field_name=name)
        out[f"{name}_from"] = df.DateFilter(field_name=name, lookup_expr="gte")
        out[f"{name}_to"] = df.DateFilter(field_name=name, lookup_expr="lte")
        order_column = name

    elif isinstance(field, models.IntegerField) and field.primary_key:
        out[name] = IntegerFilter(field_name=name)
        out[f"{name}__in"] = IntegerInFilter(field_name=name)
        order_column = name

    elif isinstance(field, (models.IntegerField, models.FloatField, models.DecimalField)):
        number = IntegerFilter if isinstance(field, models.IntegerField) else df.NumberFilter
        out[name] = number(field_name=name)
        out[f"{name}_min"] = number(field_name=name, lookup_expr="gte")
        out[f"{name}_max"] = number(field_name=name, lookup_expr="lte")
        order_column = name

    elif isinstance(field, (models.CharField, models.TextField)):
        out[name] = df.CharFilter(field_name=name, lookup_expr="icontains")
        out[f"{name}__exact"] = df.CharFilter(field_name=name, lookup_expr="exact")
        order_column = name

    elif isinstance(field, models.UUIDField):
        out[name] = df.UUIDFilter(field_name=name)
        order_column = name

    # FileField, geometry, JSON, ... fall through: no value filter, not sortable.

    if field.null:  # works for every type, including file / geometry columns
        out[f"{name}__isnull"] = df.BooleanFilter(
            field_name=name, lookup_expr="isnull", widget=BooleanWidget(),
        )

    return out, order_column


class BaseFilterSet(df.FilterSet):
    """Builds filters + ``ordering`` for every concrete field of ``Meta.model``."""

    @classmethod
    def get_fields(cls):
        # Meta.fields is not used: get_filters() below reads the model directly.
        return OrderedDict()

    @classmethod
    def get_filters(cls):
        filters = super().get_filters()
        model = cls._meta.model
        if model is None:
            return filters

        meta = getattr(cls, "Meta", None)
        skip = set(getattr(meta, "exclude_fields", ()))
        extra_ordering = getattr(meta, "extra_ordering", {})  # NEW
        order_map = OrderedDict()

        for field in (*model._meta.concrete_fields, *model._meta.many_to_many):
            if field.name in skip:
                continue
            built, order_column = _filters_for_field(field)
            for filter_name, flt in built.items():
                filters.setdefault(filter_name, flt)
            if order_column:
                order_map[order_column] = field.name

        order_map.update(extra_ordering)  # NEW: {"orm__path": "param_name"}

        if order_map:
            filters.setdefault("ordering", StableOrderingFilter(fields=order_map))
        return filters

