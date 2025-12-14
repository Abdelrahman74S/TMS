from rest_framework import serializers
from .models import Project, Task
from accounts.models import Profile
from rest_framework.exceptions import PermissionDenied

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
        
    def validate(self, data):
        request = self.context['request']
        user = request.user

        project = data.get('project')
        assigned_to = data.get('assigned_to')

        if user != project.owner and user not in project.members.all():
            raise PermissionDenied("You are not a member or owner of this project.")

        if assigned_to:
            if assigned_to != project.owner and assigned_to not in project.members.all():
                raise serializers.ValidationError({
                    "assigned_to": "Assigned user must be a project member."
                })

        return data

# Serializer for Project
class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    members = serializers.SlugRelatedField(
        many=True,
        slug_field='username',
        queryset=Profile.objects.all()
    )
    tasks = TaskSerializer(many=True, read_only=True)
    
    tasks_count_todo = serializers.SerializerMethodField()
    tasks_count_in_progress = serializers.SerializerMethodField()
    tasks_count_done = serializers.SerializerMethodField()
    tasks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id_uuid', 'title', 'description', 'owner', 'members', 'number_of_tasks',
            'tasks', 'tasks_count_todo', 'tasks_count_in_progress', 'tasks_count_done',
            'created_at', 'updated_at' , 'tasks_count'
        ]
        read_only_fields = ['owner', 'number_of_tasks', 'tasks', 'tasks_count_todo',
                            'tasks_count_in_progress', 'tasks_count_done', 'created_at', 'updated_at' ,'tasks_count']

    def get_tasks_count(self,obj):
        return obj.tasks.count()
    
    def get_tasks_count_todo(self, obj):
        return obj.tasks.filter(status='todo').count()

    def get_tasks_count_in_progress(self, obj):
        return obj.tasks.filter(status='in_progress').count()

    def get_tasks_count_done(self, obj):
        return obj.tasks.filter(status='done').count()