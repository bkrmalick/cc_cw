# Generated by Django 3.0.2 on 2020-04-04 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0009_remove_auction_createdbyusername'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='Status',
            field=models.CharField(choices=[('pending', 'PENDING'), ('live', 'LIVE'), ('completed', 'COMPLETED'), ('cancelled', 'CANCELLED')], default='pending', max_length=10),
        ),
    ]
