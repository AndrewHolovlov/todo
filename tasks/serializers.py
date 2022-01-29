from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.serializers import UserSerializer
from .models import Task, Executor, Attachment


class ExecutorField(serializers.RelatedField):
    def to_representation(self, obj):
        return {
            'id': obj.user.id,
            'full_name': obj.user.get_full_name(),
        }


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'image']


class TasksSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    executors = ExecutorField(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'content', 'author', 'executors', 'created_at', 'updated_at', 'attachments']

    def validate(self, attrs):
        attrs['author'] = self.context.get('user')
        return attrs


class TaskExecutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Executor
        fields = ['id', 'task', 'user']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('task', 'user'),
                message="User is already executor of this task"
            )
        ]
