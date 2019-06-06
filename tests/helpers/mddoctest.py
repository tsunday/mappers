from doctest import testfile
from glob import glob

from django.apps import apps
from django.conf import settings
from django.core import management


def main():
    apps.populate(settings.INSTALLED_APPS)
    management.call_command("migrate")
    markdown_files = glob("**/*.md", recursive=True)
    for markdown_file in markdown_files:
        testfile(markdown_file, module_relative=False)
