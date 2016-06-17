"""
from: https://github.com/django/django/blob/master/django/core/urlresolvers.py
"""
import warnings

from django.urls import *  # NOQA
from django.utils.deprecation import RemovedInDjango20Warning

warnings.warn(
    "Importing from django.core.urlresolvers is deprecated in favor of "
    "django.urls.", RemovedInDjango20Warning, stacklevel=2
)