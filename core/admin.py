from django.contrib import admin, messages
from django.contrib.admin.decorators import register

from core.models import NewsSource, News, ErrorTracker


@register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ('label', 'url', 'active', 'last_crawl_date')
    readonly_fields = ('active', 'last_crawl_date')

    def activate_sources(self, request, queryset):
        for obj in queryset:
            obj.active = True
            obj.save()
        self.message_user(request, "Selected sources' state has been changed to active", level=messages.ERROR)

    activate_sources.short_description = "Active selected sources for crawling"

    def deactivate_sources(self, request, queryset):
        for obj in queryset:
            obj.active = False
            obj.save()
        self.message_user(request, "Selected sources' state has been changed to active", level=messages.ERROR)

    deactivate_sources.short_description = "Active selected sources for crawling"

    actions = [activate_sources, deactivate_sources]


@register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('url', 'source', 'published_at', 'crawled_at')


@register(ErrorTracker)
class ErrorTrackerAdmin(admin.ModelAdmin):
    list_display = ('error_name', 'occurred_at')





