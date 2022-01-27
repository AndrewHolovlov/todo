from rest_framework import serializers

from accounts.serializers import TaskAuthorSerializer
from .models import Task, Executor, Attachment


class ExecutorField(serializers.RelatedField):
    def to_representation(self, obj):
        return {
            'id': obj.user.id,
            'full_name': obj.user.get_full_name(),
        }


class TasksSerializer(serializers.ModelSerializer):
    author = TaskAuthorSerializer(read_only=True)
    executors = ExecutorField(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'content', 'author', 'executors', 'created_at', 'updated_at']

    def validate(self, attrs):
        attrs['author'] = self.context.get('user')
        return attrs