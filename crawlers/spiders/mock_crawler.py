from utils.base_crawler import BaseCrawler
from datetime import datetime, timedelta
import random

class MockCrawler(BaseCrawler):
    def __init__(self):
        super().__init__('模拟数据爬虫', 'https://mock.chainflow.com')
        
        self.sources = [
            {'name': '金色财经', 'url': 'https://www.jinse.com', 'type': 'news'},
            {'name': '币世界', 'url': 'https://www.bishijie.com', 'type': 'news'},
            {'name': 'PANews', 'url': 'https://www.panewslab.com', 'type': 'news'},
            {'name': '链闻', 'url': 'https://www.chainnews.com', 'type': 'news'},
        ]
        
        self.keywords = ['比特币', '以太坊', 'DeFi', 'NFT', 'Layer2', '交易所', '挖矿', 'staking']
        self.categories = ['flash', 'article', 'market', 'report', 'announcement']

    def generate_article(self, index):
        """生成模拟文章"""
        source = random.choice(self.sources)
        main_keyword = random.choice(self.keywords)
        secondary_keyword = random.choice([k for k in self.keywords if k != main_keyword])
        
        # 文章模板
        templates = [
            f"{main_keyword}价格突破{{price}}美元，市场情绪{{sentiment}}",
            f"{main_keyword}技术分析：{{trend}}趋势确认",
            f"{main_keyword}生态最新进展：{secondary_keyword}集成完成",
            f"{main_keyword}监管动态：{{region}}发布新政策",
            f"{main_keyword}项目融资{{amount}}万美元，{{investor}}领投"
        ]
        
        template = random.choice(templates)
        title = template.format(
            price=random.randint(10000, 80000),
            sentiment=random.choice(['高涨', '谨慎', '乐观']),
            trend=random.choice(['上涨', '回调', '盘整']),
            region=random.choice(['美国', '欧洲', '亚洲']),
            amount=random.randint(500, 5000),
            investor=random.choice(['a16z', '红杉资本', '币安实验室'])
        )
        
        content = f"近日，{main_keyword}市场出现重要变化。{secondary_keyword}技术的应用为行业发展带来新的机遇。"
        content += "市场分析师认为，当前趋势有利于长期投资者，建议关注相关生态项目的发展动态。"
        content += "专家提醒投资者注意风险控制，理性参与市场交易。"
        
        # 生成发布时间（最近3天内）
        hours_ago = random.randint(1, 72)
        from django.utils import timezone
        publish_time = timezone.now() - timedelta(hours=hours_ago)
        
        return {
            'title': title,
            'content': content,
            'source_name': source['name'],
            'source_url': source['url'],
            'source_type': source['type'],
            'original_url': f"{source['url']}/news/{1000 + index}",
            'category': random.choice(self.categories),
            'tags': [main_keyword, secondary_keyword],
            'publish_time': publish_time,
            'sentiment_score': round(random.uniform(0.3, 0.9), 2),
            'importance_score': round(random.uniform(0.4, 1.0), 2)
        }

    def run(self):
        """运行模拟爬虫"""
        print(f"🧪 开始生成模拟数据...")
        
        # 健康检查
        health = self.health_check()
        print(f"📊 健康状态: {health}")
        
        # 生成5-10篇模拟文章
        article_count = random.randint(5, 10)
        success_count = 0
        
        for i in range(article_count):
            article_data = self.generate_article(i)
            if self.save_to_database(article_data):
                success_count += 1
                print(f"📄 生成文章 {i+1}/{article_count}: {article_data['title']}")
        
        print(f"✅ 模拟爬虫完成，成功生成 {success_count} 篇文章")
        return success_count
