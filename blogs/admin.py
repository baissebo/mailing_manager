from django.contrib import admin

from blogs.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "author", "title", "created_at")
    search_fields = ("slug", "author", "content")
