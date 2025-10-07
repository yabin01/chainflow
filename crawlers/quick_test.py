#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
sys.path.append('../backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chainflow_backend.settings')
django.setup()

from chainflow_backend.news.models import Article, NewsSource
from django.utils import timezone
from datetime import timedelta
import random

print("快速生成测试数据...")

# 确保有新闻来源
source, created = NewsSource.objects.get_or_create(
    name="测试来源",
    defaults={'url': 'https://test.com', 'type': 'news'}
)

# 创建几篇测试文章
titles = [
    "比特币突破重要阻力位，市场看涨情绪浓厚",
    "以太坊2.0升级进展顺利，生态持续繁荣", 
    "DeFi夏季再度来临，多个协议创新高",
    "NFT市场回暖，蓝筹项目表现强劲",
    "Layer2解决方案竞争激烈，技术迭代加速"
]

for i, title in enumerate(titles):
    article, created = Article.objects.get_or_create(
        title=title,
        defaults={
            'content': f'这是关于"{title}"的详细内容。近期市场发展迅速，投资者需要密切关注。',
            'summary': f'"{title}"相关的最新市场分析和趋势预测。',
            'source': source,
            'original_url': f'https://test.com/news/{i+1}',
            'category': random.choice(['flash', 'article', 'market']),
            'publish_time': timezone.now() - timedelta(hours=i*2)
        }
    )
    if created:
        print(f"创建: {title}")

print(f"完成！现有文章: {Article.objects.count()}篇")
