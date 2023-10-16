from django.contrib import admin
from apps.movies.models import Movie, FormatMovie


# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )


@admin.register(FormatMovie)
class FormatMovieAdmin(admin.ModelAdmin):
    list_display = (
        "id",
    )
