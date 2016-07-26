
from logging import getLogger

from dynamic_databases import settings


logger = getLogger('dynamic_databases.router')


class DynamicDatabasesRouter(object):
    # We need to identify our dynamic models
    # and point them in the right direction
    label_prefix = '{}{}'.format(settings.PREFIX, settings.SEPARATOR)

    def db_for_read(self, model, **hints):
        if model._meta.app_label.startswith(self.label_prefix):
            # We know that our app_label matches the database connection's name
            return model._meta.app_label
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label.startswith(self.label_prefix):
            # We know that our app_label matches the database connection's name
            return model._meta.app_label
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return None
