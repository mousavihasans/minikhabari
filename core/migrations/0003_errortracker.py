# Generated by Django 2.2.1 on 2019-05-19 22:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190518_1855'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorTracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error_name', models.CharField(max_length=300)),
                ('occurred_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('extra_data', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
