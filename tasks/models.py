from django.db import models

from .utils import get_file_path


class Task(models.Model):
    title = models.CharField('Title', max_length=300)
    content = models.TextField('Content')
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Executor(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='executors')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='executors')

    class Meta:
        unique_together = ('user', 'task')


class Attachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    image = models.ImageField(upload_to=get_file_path)
