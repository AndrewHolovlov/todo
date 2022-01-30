from django.urls import path

from tasks.views import TaskListView, TaskView, TaskExecutorView, CreateAttachmentView, DeleteAttachmentView


urlpatterns = [
    path('', TaskListView.as_view(), name='task_list_view'),
    path('<int:pk>/', TaskView.as_view(), name='task_view'),
    path('<int:task_id>/executors', TaskExecutorView.as_view(), name='add_task_executor_view'),
    path('<int:task_id>/attachments', CreateAttachmentView.as_view(), name='create_task_attach_image'),
    path('attachments/<int:pk>/', DeleteAttachmentView.as_view(), name='delete_task_attach_image')
]
