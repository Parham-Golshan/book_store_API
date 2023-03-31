from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price')
    list_filter = ('author',)
    search_fields = ('title', 'description', 'author__user__username')


admin.site.register(Book, BookAdmin)
