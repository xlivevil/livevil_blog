from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Files(models.Model):
    '''

    '''
    file = models.FileField(verbose_name=_('文件'), upload_to='file/%Y%m%d/')
    created = models.DateTimeField(verbose_name=_('创建时间'),
                                   default=timezone.now)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 verbose_name=_('uploader'),
                                 blank=True,
                                 null=True,
                                 related_name="%(class)s_files",
                                 on_delete=models.SET_NULL)
    is_public = models.BooleanField(_('is public'),
                                    default=True,
                                    help_text=_('not pubic'))
    is_removed = models.BooleanField(_('is removed'),
                                     default=False,
                                     db_index=True,
                                     help_text=_('removed'))

    def __repr__(self):
        return f'file-{self.file.name}'

    class Meta:
        ordering = ("-created",)
