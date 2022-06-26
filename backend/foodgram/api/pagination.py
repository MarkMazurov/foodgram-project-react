from rest_framework.pagination import PageNumberPagination


class CustomPaginationClass(PageNumberPagination):
    """Кастомная пагинация для рецептов и пользователей"""

    page_size_query_param = 'recipes_limit'
