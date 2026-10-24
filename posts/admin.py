from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "likes", "estado", "fecha_creacion")
    list_filter = ("estado", "autor__username",)
    search_fields = ("titulo",)
