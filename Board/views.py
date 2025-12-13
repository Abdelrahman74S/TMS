from django.shortcuts import render
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .ISPremission import IsProjectOwner, IsTaskCreatorOrProjectOwner
from django.db.models import Q
# Create your views here.

class ProjectView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(Q(owner=user) |Q(members=user)).distinct()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
class TaskView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
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
            self.permission_classes = [IsAuthenticated, IsProjectOwner]
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
            self.permission_classes = [IsAuthenticated, IsTaskCreatorOrProjectOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()