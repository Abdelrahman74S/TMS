from rest_framework import permissions
from .models import Project, Task

class IsProjectOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj : Project):

        return obj.owner == request.user

class IsTaskCreatorOrProjectOwner(permissions.BasePermission): 
    def has_object_permission(self, request, view, obj: Task):
        if obj.creator == request.user:
            return True
        
        if obj.project.owner == request.user:
            return True
            
        return False
    
class IsProjectAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Project):
        if obj.owner == request.user:
            return True  
        membership = obj.memberships.filter(user=request.user, role='admin').first()
        return membership is not None
