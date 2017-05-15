
from logging import getLogger

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from dynamic_databases.models import DynamicDatabaseConfig


logger = getLogger('dynamic_databases.receivers')


@receiver([pre_save, pre_delete], sender=DynamicDatabaseConfig)
def unregister_database(sender, **kwargs):
    if 'instance' in kwargs and kwargs['instance'].pk is not None:
        kwargs['instance'].unregister()
