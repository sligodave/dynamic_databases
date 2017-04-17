from __future__ import unicode_literals

from logging import getLogger
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.core.management.commands.inspectdb import Command
from django.db import models, connections
from django.apps import AppConfig
from django.apps.registry import apps
from django import VERSION

from jsonfield import JSONField

from dynamic_databases import settings


logger = getLogger('dynamic_databases.models')


class AbstractDatabase(models.Model):
    name = models.CharField(max_length=256)
    config = JSONField()

    class Meta:
        ordering = ('name', 'id')
        abstract = True

    def __unicode__(self):
        return self.name

    @property
    def connection(self):
        self.register()
        return connections[self.label]

    @property
    def tables(self):
        cursor = self.connection.cursor()
        cursor.execute('SHOW TABLES;')
        tables = []
        for row in cursor.fetchall():
            tables.append(row[0])
        return tables

    def register(self):
        # Do we have this database registered yet
        if self.label not in connections._databases:
            # Register the database
            connections._databases[self.label] = self.config
            # Break the cached version of the database dict so it'll find our new database
            del connections.databases
        # Have we registered our fake app that'll hold the models for this database
        if self.label not in apps.app_configs:
            # We create our own AppConfig class, because the Django one needs a path to the module that is the app.
            # Our dummy app obviously doesn't have a path
            AppConfig2 = type(
                'AppConfig'.encode('utf8'), (AppConfig,), {'path': '/tmp/{}'.format(self.label)}
            )
            app_config = AppConfig2(self.label, self.label)
            app_config.apps = apps
            # Manually register the app with the running Django instance
            apps.app_configs[self.label] = app_config
            apps.app_configs[self.label].models = {}

    def unregister(self):
        logger.info('Unregistering Database, app and all related models: "%s"', self.label)
        if self.label in apps.app_configs:
            del apps.app_configs[self.label]
        if self.label in apps.all_models:
            del apps.all_models[self.label]
        if self.label in connections._databases:
            del connections._databases[self.label]
            del connections.databases

    @property
    def label(self):
        # We want to be able to identify the dynamic databases and apps
        # So we prepend their names with a common string
        return '{}{}{}'.format(settings.PREFIX, settings.SEPARATOR, self.pk)

    def get_model(self, table_name):
        # Ensure the database connect and it's dummy app are registered
        self.register()
        model_name = table_name.lower().replace('_', '')

        # Is the model already registered with the dummy app?
        if model_name not in apps.all_models[self.label]:
            logger.info('Adding dynamic model: %s %s', self.label, table_name)

            # Use the "inspectdb" management command to get the structure of the table for us.
            file_obj = StringIO()
            kwargs = {
                'database': self.label,
                'table_name_filter': lambda t: t == table_name
            }
            if VERSION[0] >= 1 and VERSION[1] >= 10:
                kwargs['table'] = [table_name]
            Command(stdout=file_obj).handle(**kwargs)
            model_definition = file_obj.getvalue()
            file_obj.close()

            # Make sure that we found the table and have a model definition
            loc = model_definition.find('(models.Model):')
            if loc != -1:
                # Ensure that the Model has a primary key.
                # Django doesn't support multiple column primary keys,
                # So we have to add a primary key if the inspect command didn't
                if model_definition.find('primary_key', loc) == -1:
                    loc = model_definition.find('(', loc + 14)
                    model_definition = '{}primary_key=True, {}'.format(
                        model_definition[:loc + 1], model_definition[loc + 1:]
                    )
                # Ensure that the model specifies what app_label it belongs to
                loc = model_definition.find('db_table = \'{}\''.format(table_name))
                if loc != -1:
                    model_definition = '{}app_label = \'{}\'\n        {}'.format(
                        model_definition[:loc], self.label, model_definition[loc:]
                    )

                # Register the model with Django. Sad day when we use 'exec'
                # exec(model_definition, globals(), locals())
                exec model_definition in globals(), locals()
                # Update the list of models that the app
                # has to match what Django now has for this app
                apps.app_configs[self.label].models = apps.all_models[self.label]
            else:
                logger.info('Could not find table: %s %s', self.label, table_name)
        else:
            logger.info('Already added dynamic model: %s %s', self.label, table_name)

        # If we have the connection, app and model. Return the model class
        if (
                self.label in connections._databases and
                self.label in apps.all_models and
                model_name in apps.all_models[self.label]
        ):
            return apps.get_model(self.label, model_name)


class Database(AbstractDatabase):
    pass
