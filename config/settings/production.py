from .base import *

import django_heroku

ALLOWED_HOSTS = ['https://todo-test-task.herokuapp.com/']

django_heroku.settings(locals())
