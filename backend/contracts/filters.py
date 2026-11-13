"""
project/filters.py

FilterSets for the project app. The generic machinery (BaseFilterSet, which
builds a filter for every model field, plus the typed filters) lives in
common/filters.py; see the table at the top of that file for the URL
parameters it generates. This file only lists the models and the few filters
that are specific to this app.
"""
from decimal import Decimal

from django.db.models import (
    Q,DecimalField, ExpressionWrapper, F, OuterRef, Subquery, Sum, Value,
    Case, When, IntegerField,Exists
)
from django.db.models.functions import Coalesce
import django_filters as df

from common.filters import BaseFilterSet, IntegerFilter , IntegerInFilter
from rest_framework import serializers

from contracts.models.SharhKhadamats import (
    ShrhCatalog
)

# ---------------------------------------------------------------------------
# Simple lookup/domain tables
# ---------------------------------------------------------------------------

class ShrhCatalogFilterSet(BaseFilterSet):

    class Meta:
        model = ShrhCatalog

