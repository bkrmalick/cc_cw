# Generated by Django 3.0.2 on 2020-04-02 02:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0007_auto_20200402_0244'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='PlacedByUser',
            new_name='PlacedByUserID',
        ),
    ]
