# Generated by Django 2.2.5 on 2019-12-10 20:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('is_deleted', models.BooleanField(blank=True, default=False)),
                ('phone_number', models.CharField(max_length=30)),
                ('available_balance', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='available_balance')),
                ('actual_balance', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='actual_balance')),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
