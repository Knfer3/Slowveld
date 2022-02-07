from django.contrib import admin
from .models import Blog, Status, Category


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status',)
    list_filter = ('status',)
    search_fields = ('title', 'content',)

admin.site.register(Status )
admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)