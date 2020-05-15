# Generated by Django 2.2 on 2020-05-12 19:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_postcomment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomment',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_type_set_for_postcomment', to='contenttypes.ContentType', verbose_name='content type'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='postcomment_comments', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
