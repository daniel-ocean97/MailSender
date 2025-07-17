from django.contrib import admin

from .models import Client, Mailing, Letter, Logging


@admin.register(Client)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "owner")
    list_filter = ("email",)
    search_fields = ("email", "full_name")


@admin.register(Mailing)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("start_time", "status", "message")
    search_fields = ("message",)


@admin.register(Letter)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("theme", "text", "owner")
    search_fields = ("theme",)


@admin.register(Logging)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("time", "status", "owner")
    search_fields = ("owner",)
