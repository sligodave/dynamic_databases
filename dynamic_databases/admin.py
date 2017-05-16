
from logging import getLogger
from json import dumps

from django.contrib import admin

from dynamic_databases.models import DynamicDatabaseConfig


logger = getLogger('dynamic_databases.admin')


def engine(obj):
    return obj.config.get('engine', obj.config.get('ENGINE'))
engine.short_description = 'Engine'


def config(obj):
    return dumps(obj.config)
config.short_description = 'Config'


class DynamicDatabaseConfigAdmin(admin.ModelAdmin):
    list_display = ('name', engine, config)


admin.site.register(DynamicDatabaseConfig, DynamicDatabaseConfigAdmin)
