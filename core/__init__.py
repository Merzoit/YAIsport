# __init__.py
from __future__ import absolute_import, unicode_literals

# Этот импорт нужен, чтобы обеспечить корректную работу Celery с Django.
from .celery import app as celery_app

__all__ = ('celery_app',)
