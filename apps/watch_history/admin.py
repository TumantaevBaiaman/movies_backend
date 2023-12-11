from django.contrib import admin

from apps.watch_history.models import WatchHistory

@admin.register(WatchHistory)
class AdminWatchHistory(admin.ModelAdmin):
    list_display = ("id", "user", "timestamp")
