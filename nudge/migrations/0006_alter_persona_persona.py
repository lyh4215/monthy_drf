# Generated by Django 5.0 on 2024-08-31 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nudge', '0005_alter_nudge_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='persona',
            field=models.TextField(),
        ),
    ]
