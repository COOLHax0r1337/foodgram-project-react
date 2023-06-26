from rest_framework.pagination import PageNumberPagination

RECIPES_PER_PAGE = 6


class PgLimPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = RECIPES_PER_PAGE
