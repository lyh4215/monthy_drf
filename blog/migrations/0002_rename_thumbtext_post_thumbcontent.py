# Generated by Django 5.0 on 2024-02-24 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='thumbText',
            new_name='thumbContent',
        ),
    ]
