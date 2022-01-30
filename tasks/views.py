import logging

from PIL import Image
from rest_framework import generics, status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from accounts.models import User
from .models import Task, Executor, Attachment
from .serializers import TasksSerializer, TaskExecutorSerializer
from config.utils import send_email

logger = logging.getLogger(__name__)


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

    @swagger_auto_schema(
        operation_id='task_by_id',
        operation_description='Get task by id',
        responses={
            200: TasksSerializer,
            404: 'Task does not exist',
            400: 'Bad request',
        }
    )
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id='task_update',
        operation_description='Update a task by id',
        responses={
            200: TasksSerializer,
            404: 'Task does not exist',
            400: 'Bad request',
            403: 'You are not author of this task'
        }
    )
    def put(self, request, *args, **kwargs):
        task = self.get_object()
        user = self.request.user
        if task.author != user:
            raise exceptions.PermissionDenied('You are not author of this task')
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id='task_delete',
        operation_description='Delete a task by id',
        responses={
            404: 'Task does not exist',
            400: 'Bad request',
            403: 'You are not author of this task'
        }
    )
    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        user = self.request.user
        if task.author != user:
            raise exceptions.PermissionDenied('You are not author of this task')
        return super().delete(request, *args, **kwargs)


class TaskExecutorView(APIView):
    queryset = Executor.objects.all()
    serializer_class = TaskExecutorSerializer

    @swagger_auto_schema(
        operation_id='task_executor_create',
        operation_description='Add executor to task',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='user id')},
            required=['user']
        ),
        responses={
            200: TasksSerializer,
            400: 'Bad request',
            403: 'You are not author of this task',
            404: 'Task does not exist'
        }
    )
    def post(self, request, task_id, *args, **kwargs):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise exceptions.NotFound('Task does not exist')

        if task.author != request.user:
            raise exceptions.PermissionDenied('You are not author of this task')

        serializer = self.serializer_class(data={**request.data, 'task': task_id})
        if serializer.is_valid():
            executor = serializer.save()

            try:
                send_email(subject='New task', user=executor.user.email, template='add_executor.html',
                           content={
                               'full_name': executor.user.get_full_name(),
                               'task_title': executor.task.title,
                               'task_link': 'not_implemented_yet'
                           })
            except Exception as e:
                logger.error(e, exc_info=True)

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_id='task_executor_delete',
        operation_description='Delete executor from task',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='user id')},
            required=['user']
        ),
        responses={
            204: '',
            400: 'Bad request',
            403: 'You are not author of this task',
            404: 'Task does not exist or User does not exist'
        }
    )
    def delete(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise exceptions.NotFound('Task does not exist')

        if task.author != request.user:
            raise exceptions.PermissionDenied('You are not author of this task')

        if user_id := request.data.get('user', None):
            if not User.objects.filter(id=user_id).exists():
                raise exceptions.NotFound('User does not exist')
        else:
            raise exceptions.ValidationError('user field is required')

        if executor := Executor.objects.filter(task=task_id, user=user_id):
            executor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise exceptions.ValidationError('User is not executor of this task')


class CreateAttachmentView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id='task_attach_image',
        operation_description='Attach image to task',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'image': openapi.Schema(type=openapi.TYPE_FILE, description='image')},
            required=['image']
        ),
        responses={
            200: openapi.Schema(type=openapi.TYPE_OBJECT,
                                properties={'image_url': openapi.Schema(type=openapi.FORMAT_URI)}),
            400: 'The image can have a maximum size of 5 MB and the following formats: PNG, JPG, JPEG, SVG',
            403: 'You are not author of this task',
            404: 'Task does not exist'
        }
    )
    def post(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise exceptions.NotFound('Task does not exist')

        if task.author != request.user:
            raise exceptions.PermissionDenied('You are not author of this task')

        try:
            uploaded_photo = Image.open(request.data['image'])
            format_ = uploaded_photo.format
            if format_.lower() not in ('png', 'jpg', 'jpeg', 'svg') or request.FILES['image'].size > 5000000:
                raise exceptions.ValidationError(
                    'The image can have a maximum size of 5 MB and the following formats: PNG, JPG, JPEG, SVG')
            attach = Attachment.objects.create(task=task, image=request.data['image'])
            return Response({"image_url": attach.image.url}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e, exc_info=True)
            raise exceptions.ValidationError('Something went wrong')


class DeleteAttachmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Attachment.objects.get(id=self.kwargs['pk'])
        except Attachment.DoesNotExist:
            raise exceptions.NotFound('Attachment does not exist')

    @swagger_auto_schema(
        operation_id='task_delete_image',
        operation_description='Delete image from task',
        responses={
            204: '',
            400: 'Bad request',
            403: 'You are not author of this task',
            404: 'Attachment does not exist'
        }
    )
    def delete(self, request, *args, **kwargs):
        attachment = self.get_object()
        if attachment.task.author != request.user:
            raise exceptions.PermissionDenied('You are not author of this task')
        attachment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







