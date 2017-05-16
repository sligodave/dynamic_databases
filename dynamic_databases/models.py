from __future__ import unicode_literals

from logging import getLogger

from django.db import models
from jsonfield import JSONField

from dynamic_databases.database import DynamicDatabase


logger = getLogger('dynamic_databases.models')


class AbstractDynamicDatabaseConfig(models.Model):
    name = models.CharField(max_length=256)
    config = JSONField()

    class Meta:
        ordering = ('name', 'id')
        abstract = True

    def __unicode__(self):
        return self.name

    @property
    def dynamic_database(self):
        return DynamicDatabase(
            name='{}_{}'.format(self.pk, self.name), config=self.config
        )


class DynamicDatabaseConfig(AbstractDynamicDatabaseConfig):
    pass
