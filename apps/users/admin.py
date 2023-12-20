from django.contrib import admin
from apps.users.models import User, Subscription, Notification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id",)