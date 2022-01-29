from django.urls import path

from tasks.views import TaskListView, TaskView, TaskExecutorView, AttachmentView


urlpatterns = [
    path('', TaskListView.as_view(), name='task_list_view'),
    path('<int:pk>/', TaskView.as_view(), name='task_view'),
    path('<int:task_id>/executors', TaskExecutorView.as_view(), name='add_task_executor_view'),
    path('<int:task_id>/attach-image', AttachmentView.as_view(), name='task_attach_image')

]
