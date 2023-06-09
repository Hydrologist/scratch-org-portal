# Generated by Django 4.1.5 on 2023-02-16 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=200)),
                ('access_url', models.URLField(max_length=250)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('dev_hub', models.BooleanField(default=False)),
                ('expiration_date', models.DateTimeField()),
                ('instance_url', models.URLField()),
                ('login_url', models.URLField(max_length=100)),
                ('organization_id', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SalesforceUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('profile_name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('primary_user', models.BooleanField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scratchorgs.organization')),
            ],
        ),
    ]
