# Generated by Django 3.0.2 on 2020-03-08 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='RegisteredDate',
        ),
    ]