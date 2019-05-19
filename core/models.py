from django.db import models
from django.utils.timezone import now


class NewsSource(models.Model):
    label = models.CharField(max_length=100, unique=True)
    url = models.CharField(max_length=1000, unique=True)
    active = models.BooleanField(default=True)
    last_crawl_date = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return self.label


class News(models.Model):
    url = models.URLField(max_length=1000, unique=True)
    source = models.ForeignKey(NewsSource, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=1000)
    news_id = models.CharField(max_length=1000, blank=True, null=True)
    content = models.TextField(help_text='content format is JSON.')
    published_at = models.DateTimeField(default=now)
    crawled_at = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.source.label+'-'+self.title[0:49])

    class Meta:
        verbose_name_plural = "News"


class ErrorTracker(models.Model):
    error_name = models.CharField(max_length=300)
    occurred_at = models.DateTimeField(default=now)
    extra_data = models.TextField(blank=True, null=True)
