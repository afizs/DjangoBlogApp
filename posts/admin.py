from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp', 'updated')
    list_display_links = ['timestamp']
    list_filter = ['timestamp', 'updated']
    search_fields = ['content', 'title']
    class Meta:
        model = Post

# Register your models here.
admin.site.register(Post, PostAdmin)
