from django.contrib import admin, messages
from django.contrib.admin.decorators import register

from core.models import NewsSource, News

# from celery.task.schedules import crontab
# from celery.decorators import periodic_task
#
# def crawling_news()
#
#     @periodic_task(run_every=(crontab(second='*/15')), name="some_task", ignore_result=True)
#     def some_task():


# do something

@register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ('label', 'url', 'active', 'last_crawl_date')
    # readonly_fields = ('title',)

    def start_schedule_crawling(self, request, queryset):
        if len(queryset) != 1:
            self.message_user(request, 'please select 1 news source.', level=messages.ERROR)
            return
        # crawling_news()

    start_schedule_crawling.short_description = "Start Crawling news every 5 minutes"

    actions = [start_schedule_crawling]


@register(News)
class NewsAdmin(admin.ModelAdmin):
    pass





