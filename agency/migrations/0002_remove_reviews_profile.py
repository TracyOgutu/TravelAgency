# Generated by Django 2.2 on 2020-10-10 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviews',
            name='profile',
        ),
    ]
