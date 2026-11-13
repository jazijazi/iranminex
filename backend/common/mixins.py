from django.db.models import Q
from django.core.exceptions import ValidationError

class SearchMixin:
    """
    Adds search functionality to any APIView.
    
    Usage:
        - set `search_fields` in your view class
        - call `self.apply_search(queryset, request)` in your get method
        - all URL addreses from url must come with ?search=<search string>
    """
    search_fields = []  # override this in your view

    def apply_search(self, queryset, request):
        search = request.query_params.get('search', '').strip()
        
        if not search or not self.search_fields:
            return queryset
        
        query = Q()
        for field in self.search_fields:
            query |= Q(**{f"{field}__icontains": search})
        
        return queryset.filter(query).distinct()
    
    
class FilterMixin:
    """
    Apply a django-filter FilterSet to a queryset in APIView classes.

    Set `filterset_class` in the view, then call `apply_filters()`
    with the current queryset and request. If no filterset is defined,
    the original queryset is returned unchanged.

    Example:
        class ContractListViews(DjangoFilterMixin, APIView):
            filterset_class = ContractFilter

            def get(self, request):
                queryset = Contract.objects.all()
                queryset = self.apply_filters(queryset, request)
                ...
    """
    filterset_class = None

    def apply_filterset(self, queryset, request):
        if not self.filterset_class:
            return queryset
        fs = self.filterset_class(
            request.query_params,
            queryset=queryset,
            request=request,
        )
        if not fs.is_valid():
            raise ValidationError(fs.errors)
        return fs.qs