from django.contrib import admin

from .models import User


@admin.register(User)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("email",)
    list_filter = ("email",)
    search_fields = ("email",)
