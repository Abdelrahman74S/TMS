from django.db import models
from accounts.models import Profile
import uuid

# Create your models here.

class Project(models.Model):
    id_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(Profile ,on_delete=models.CASCADE, related_name='owned_projects')
    members = models.ManyToManyField(Profile, related_name='member_of_projects')
    number_of_tasks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Task(models.Model):
    id_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ManyToManyField(Profile, related_name='assigned_tasks') # ManyToManyField
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_tasks')
    status = models.CharField(max_length=50, choices=[('todo', 'To Do'), ('in_progress', 'In Progress'), ('done', 'Done')], default='todo')
    priority = models.CharField(max_length=50, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
   
class ProjectMember(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=[('member','Member'), ('admin','Admin')], default='member')
