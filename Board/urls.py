from django.urls import path
from .views import ProjectView, TaskView, ProjectDetailView, TaskDetailView

urlpatterns = [
    path('projects/', ProjectView.as_view(), name='project-list'),
    path('tasks/', TaskView.as_view(), name='task-list'),
    path('projects/<uuid:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('tasks/<uuid:pk>/', TaskDetailView.as_view(), name='task-detail'),
]