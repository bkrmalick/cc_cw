# Generated by Django 3.0.2 on 2020-03-25 00:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('actions', '0006_auto_20200319_0011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='ItemCondition',
        ),
        migrations.AddField(
            model_name='item',
            name='ItemCondition',
            field=models.CharField(choices=[('poor', 'POOR'), ('good', 'GOOD'), ('new', 'NEW')], default='good', max_length=5),
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BidPrice', models.FloatField()),
                ('Auction1', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='actions.Auction')),
                ('PlacedByUsername', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='auction',
            name='WinnerBid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='actions.Bid'),
        ),
    ]
