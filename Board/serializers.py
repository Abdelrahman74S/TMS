from rest_framework import serializers
from .models import Project, Task
from accounts.models import Profile

# Serializer for Task
class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='creator.username', read_only=True)
    assigned_to = serializers.CharField(source='assigned_to.username', read_only=True)
    project_title = serializers.CharField(source='project.title', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id_uuid', 'title', 'description', 'project', 'project_title',
            'status', 'priority', 'creator', 'assigned_to', 'created_at', 'updated_at'
        ]
        read_only_fields = ['creator', 'created_at', 'updated_at']

# Serializer for Project
class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='ownerusername', read_only=True)
    members = serializers.SlugRelatedField(
        many=True,
        slug_field='username',
        queryset=Profile.objects.all()
    )
    tasks = TaskSerializer(many=True, read_only=True)
    
    tasks_count_todo = serializers.SerializerMethodField()
    tasks_count_in_progress = serializers.SerializerMethodField()
    tasks_count_done = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id_uuid', 'title', 'description', 'owner', 'members', 'number_of_tasks',
            'tasks', 'tasks_count_todo', 'tasks_count_in_progress', 'tasks_count_done',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'number_of_tasks', 'tasks', 'tasks_count_todo',
                            'tasks_count_in_progress', 'tasks_count_done', 'created_at', 'updated_at']

    def get_tasks_count_todo(self, obj):
        return obj.tasks.filter(status='todo').count()

    def get_tasks_count_in_progress(self, obj):
        return obj.tasks.filter(status='in_progress').count()

    def get_tasks_count_done(self, obj):
        return obj.tasks.filter(status='done').count()