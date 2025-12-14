from rest_framework.pagination import PageNumberPagination

class ProjectPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 10
    page_query_param = 'page_project'
    page_size_query_param = 'page_size_project'
    
class TaskPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 10
    page_query_param = 'page_Task'
    page_size_query_param = 'page_size_Task'