from django.db.models import Q

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