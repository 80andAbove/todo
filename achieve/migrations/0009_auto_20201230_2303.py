# Generated by Django 3.1.1 on 2020-12-30 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achieve', '0008_auto_20201230_2301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
