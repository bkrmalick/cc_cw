# Generated by Django 3.0.2 on 2020-03-26 01:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('actions', '0004_auction_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='CreatedByUserID',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='auction',
            name='CreatedByUsername',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='auction',
            name='Item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='actions.Item'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='WinnerBid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='actions.Bid'),
        ),
    ]