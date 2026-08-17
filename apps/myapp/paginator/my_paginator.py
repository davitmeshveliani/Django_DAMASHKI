from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class TaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5

# ახალი LimitOffsetPagination
class TaskLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 5