# Generated by Django 2.2.3 on 2019-07-28 23:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unitRate', models.FloatField(default=None)),
                ('currency_from', models.CharField(max_length=50)),
                ('currency_to', models.CharField(default='Gourdes', max_length=50)),
                ('rate_set', models.DateField(auto_now=True)),
                ('rate_status', models.BooleanField(default=True)),
                ('rate_description', models.CharField(default=None, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transfer_Date', models.DateField(auto_now=True)),
                ('transfer_origin', models.CharField(default=None, max_length=50)),
                ('transfer_originAmount', models.FloatField(default=None)),
                ('transfer_givenAmount', models.FloatField(default=None)),
                ('rate', models.FloatField(default=None)),
                ('transfer_comment', models.TextField(null=True)),
                ('transfer_by', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
