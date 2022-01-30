from django.contrib import admin

from .models import Task, Executor, Attachment

admin.site.register(Task)
admin.site.register(Executor)
admin.site.register(Attachment)
