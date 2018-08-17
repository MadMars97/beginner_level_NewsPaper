from django.contrib import admin
from . import models

# Register your models here.

#StackedInline each field has its own line , TabularInline all model fields appear on one line
class CommentInline(admin.TabularInline):
    model = models.Comment

class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]

class ReplyInline(admin.TabularInline):
    model = models.Reply

class CommentAdmin(admin.ModelAdmin):
    inlines = [
        ReplyInline,
    ]


admin.site.register(models.Article,ArticleAdmin)
admin.site.register(models.Comment,CommentAdmin)
admin.site.register(models.Reply)