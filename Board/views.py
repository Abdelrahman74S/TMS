from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .ISPremission import IsProjectOwner, IsTaskCreatorOrProjectOwner , IsProjectAdmin
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import ProjectPagination, TaskPagination
# Create your views here.

class ProjectView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    # filter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['owner', 'members']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'number_of_tasks']
    
    # pagination
    pagination_class = ProjectPagination

    
    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(owner=user) |Q(members=user)).distinct()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
class TaskView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['project', 'status', 'priority']
    search_fields = ['title', 'description' , 'assigned_to__username' , 'creator__username']
    ordering_fields = ['created_at']
    
    pagination_class = TaskPagination

    def get_queryset(self):
        user = self.request.user

        return Task.objects.filter(
            Q(creator=user) | 
            Q(assigned_to=user) |
            Q(project__owner=user) |   
            Q(project__members=user)   
        ).distinct()    
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(owner=user) | Q(members=user)).distinct()
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated, IsProjectOwner , IsProjectAdmin]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(creator=user) | 
            Q(assigned_to=user) |
            Q(project__owner=user) |
            Q(project__members=user)
        ).distinct()
        
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated, IsTaskCreatorOrProjectOwner , IsProjectAdmin]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()