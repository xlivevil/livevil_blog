# Generated by Django 2.2 on 2020-07-05 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20200512_1922'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postcomment',
            old_name='create_time',
            new_name='created_time',
        ),
    ]
