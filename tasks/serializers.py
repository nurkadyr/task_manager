from rest_framework import serializers
from .models import Task, Comment, TaskFile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        ref_name = 'TaskUser'

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), source='assigned_to')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'assigned_to', 'assigned_to_id', 'completed', 'deadline', 'reminder']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'task', 'author', 'text', 'created_at']

class TaskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskFile
        fields = ['id', 'task', 'file', 'uploaded_at']
