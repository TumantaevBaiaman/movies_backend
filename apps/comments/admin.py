from django.contrib import admin

from apps.comments.models import Comment, CommentSeries


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'movie',
        'rating'
    )


@admin.register(CommentSeries)
class CommentSeriesAdmin(admin.ModelAdmin):
    list_display = (
        'series',
        'rating'
    )