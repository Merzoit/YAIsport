from __future__ import absolute_import, unicode_literals

# Это гарантирует, что приложение всегда импортирует приложение Celery
# когда Django запускается
from .celery import app as celery_app

__all__ = ('celery_app',)