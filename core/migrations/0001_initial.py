# Generated by Django 2.2.1 on 2019-05-18 09:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, unique=True)),
                ('url', models.CharField(max_length=1000, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('news_id', models.CharField(max_length=1000)),
                ('content', models.TextField(help_text='content format is JSON.')),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.NewsSource')),
            ],
        ),
    ]
