import os
import uuid

from rest_framework.permissions import BasePermission


def get_file_path(instance, filename):
    """
    Rename images
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(instance.__class__.__name__.lower(), filename)
