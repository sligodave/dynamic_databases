from __future__ import unicode_literals

from django.apps import AppConfig


class DynamicDatabasesConfig(AppConfig):
    name = 'dynamic_databases'

    def ready(self):
        import dynamic_databases.receivers
