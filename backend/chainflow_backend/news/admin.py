from django.contrib import admin
from .models import NewsSource, Article

@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'is_active', 'created_at']
    list_filter = ['type', 'is_active']
    search_fields = ['name']
    list_editable = ['is_active']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'category', 'publish_time', 'view_count', 'is_active']
    list_filter = ['source', 'category', 'publish_time', 'is_active']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'publish_time'
    list_editable = ['is_active']
    
    fieldsets = (
        ('基础信息', {
            'fields': ('title', 'content', 'summary')
        }),
        ('来源信息', {
            'fields': ('source', 'original_url', 'category')
        }),
        ('时间信息', {
            'fields': ('publish_time',)
        }),
        ('统计信息', {
            'fields': ('view_count', 'like_count')
        }),
        ('分析信息', {
            'fields': ('sentiment_score', 'importance_score')
        }),
        ('状态信息', {
            'fields': ('is_active', 'is_verified')
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
