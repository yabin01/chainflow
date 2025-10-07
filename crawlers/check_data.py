#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
sys.path.append('../backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chainflow_backend.settings')
django.setup()

from chainflow_backend.news.models import Article, NewsSource

print("=== 数据状态检查 ===")
print(f"新闻来源数量: {NewsSource.objects.count()}")
print(f"文章总数: {Article.objects.count()}")

print("\n=== 最新5篇文章 ===")
articles = Article.objects.all().order_by('-publish_time')[:5]
for article in articles:
    print(f"- {article.title} ({article.publish_time})")

print("\n=== 按分类统计 ===")
from django.db.models import Count
category_stats = Article.objects.values('category').annotate(count=Count('id'))
for stat in category_stats:
    print(f"- {stat['category']}: {stat['count']}篇")
