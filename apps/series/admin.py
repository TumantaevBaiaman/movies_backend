from django.contrib import admin
from apps.series.models import Series, Season, SeriesVideo


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("id", "series", "season")


@admin.register(SeriesVideo)
class SeriesVideoAdmin(admin.ModelAdmin):
    list_display = ("id", "series")
