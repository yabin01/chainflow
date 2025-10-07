from django.db import models
from django.utils import timezone

class NewsSource(models.Model):
    SOURCE_TYPES = [
        ('news', '新闻资讯'),
        ('social', '社交媒体'),
        ('official', '官方公告'),
        ('analysis', '分析研报'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='来源名称')
    url = models.URLField(verbose_name='来源网址')
    type = models.CharField(max_length=20, choices=SOURCE_TYPES, default='news', verbose_name='来源类型')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '新闻来源'
        verbose_name_plural = '新闻来源'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('flash', '快讯'),
        ('article', '文章'),
        ('report', '研报'),
        ('announcement', '公告'),
        ('market', '行情'),
    ]
    
    # 基础信息
    title = models.CharField(max_length=500, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    summary = models.TextField(blank=True, verbose_name='摘要')
    
    # 来源信息
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE, verbose_name='来源')
    original_url = models.URLField(unique=True, verbose_name='原文链接')
    
    # 分类信息
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='article', verbose_name='分类')
    tags = models.JSONField(default=list, blank=True, verbose_name='标签')
    
    # 时间信息
    publish_time = models.DateTimeField(default=timezone.now, verbose_name='发布时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    # 统计信息
    view_count = models.IntegerField(default=0, verbose_name='浏览次数')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    
    # 分析字段
    sentiment_score = models.FloatField(null=True, blank=True, verbose_name='情感得分')
    importance_score = models.FloatField(default=0.0, verbose_name='重要程度')
    
    # 状态字段
    is_active = models.BooleanField(default=True, verbose_name='是否显示')
    is_verified = models.BooleanField(default=False, verbose_name='是否核实')
    
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-publish_time']
        indexes = [
            models.Index(fields=['publish_time']),
            models.Index(fields=['category']),
            models.Index(fields=['source']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # 自动生成摘要（如果为空）
        if not self.summary and self.content:
            self.summary = self.content[:200] + '...' if len(self.content) > 200 else self.content
        super().save(*args, **kwargs)
