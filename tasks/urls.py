from django.urls import path

from tasks.views import TaskListView, TaskView

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list_view'),
    path('<int:pk>/', TaskView.as_view(), name='task_view'),
]
