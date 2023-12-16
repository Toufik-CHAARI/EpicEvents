# Generated by Django 5.0 on 2023-12-15 11:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('company_name', models.CharField(max_length=255)),
                ('creation_date', models.DateField()),
                ('last_update', models.DateField()),
                ('sales_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('remaining_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('creation_date', models.DateField()),
                ('is_signed', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.client')),
                ('sales_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contracts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('location', models.CharField(max_length=255)),
                ('attendees', models.IntegerField()),
                ('notes', models.TextField()),
                ('client_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='crm.client')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.contract')),
                ('support_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supported_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]