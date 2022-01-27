from rest_framework import generics, status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import TasksSerializer
from .models import Task, Executor, Attachment


class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TasksSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class TaskView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TasksSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        user = self.request.user
        if task.author != user:
            raise exceptions.PermissionDenied('You are not author of this task')
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        user = self.request.user
        if task.author != user:
            raise exceptions.PermissionDenied('You are not author of this task')
        return super().delete(request, *args, **kwargs)

