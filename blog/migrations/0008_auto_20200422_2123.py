# Generated by Django 2.2.11 on 2020-04-22 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20200422_2112'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postviewinfo',
            options={'ordering': ['view_time'], 'verbose_name': '浏览记录', 'verbose_name_plural': '浏览记录'},
        ),
        migrations.RenameField(
            model_name='postviewinfo',
            old_name='view',
            new_name='view_time',
        ),
    ]
