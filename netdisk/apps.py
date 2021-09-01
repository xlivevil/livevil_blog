from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NetdiskConfig(AppConfig):
    name = 'netdisk'
    verbose_name = _('网盘')
