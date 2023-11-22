from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


def paginate_queryset(request, queryset):
    paginator = CustomPagination()
    paginated_data = paginator.paginate_queryset(queryset, request)
    if paginated_data is not None:
        count = paginator.page.paginator.count
        next_page = paginator.get_next_link()
        previous_page = paginator.get_previous_link()
        return {
            'count': count,
            'next': next_page,
            'previous': previous_page,
            'results': paginated_data
        }
    count = queryset.count()
    return {
        'count': count,
        'next': None,
        'previous': None,
        'results': queryset
    }


def get_filters(request, filters):
    return {key: value for key, value in filters.items() if value}