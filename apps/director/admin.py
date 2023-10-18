from django.contrib import admin

from apps.director.models import Director


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
