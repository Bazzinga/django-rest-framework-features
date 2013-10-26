from django.contrib import admin

from .models import Tag, Article, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'category')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)