# Generated by Django 4.1.5 on 2023-05-09 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scratchorgs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='alias',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='organization',
            name='expired_flag',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='organization',
            name='is_dev_hub',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='organization',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='username',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='organization',
            name='dev_hub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scratchorgs.organization'),
        ),
    ]
