from django.contrib import admin  # type: ignore
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug','url')
    search_fields = ('title', 'author')
    readonly_fields = ('slug',)
