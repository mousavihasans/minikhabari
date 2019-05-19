# Generated by Django 2.2.1 on 2019-05-18 18:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='crawled_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='news',
            name='url',
            field=models.URLField(default='url', max_length=1000, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='newssource',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='newssource',
            name='last_crawl_date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='news_id',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]