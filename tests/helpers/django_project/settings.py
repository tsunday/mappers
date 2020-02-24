# -*- coding: utf-8 -*-
INSTALLED_APPS = ["django_project.apps.ProjectConfig"]

SECRET_KEY = "*"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
