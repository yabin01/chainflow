from utils.base_crawler import BaseCrawler
from datetime import datetime
import random

class TestCrawler(BaseCrawler):
    def __init__(self):
        super().__init__('测试爬虫', 'https://test.chainflow.com')
    
    def run(self):
        logger = self.__class__.__module__
        print(f"开始运行 {self.name}...")
        
        # 健康检查
        health = self.health_check()
        print(f"健康状态: {health}")
        
        # 生成测试数据
        test_articles = [
            {
                'title': '比特币突破关键阻力位，市场情绪转向积极',
                'content': '近日比特币价格成功突破45000美元关键阻力位，技术指标显示市场情绪明显改善。分析师认为，这一突破可能开启新一轮上涨行情。',
                'source_name': '测试财经',
                'source_url': 'https://test.com',
                'source_type': 'news',
                'original_url': 'https://test.com/news/1001',
                'category': 'market',
                'tags': ['比特币', '技术分析'],
                'publish_time': datetime.now(),
                'sentiment_score': 0.75,
                'importance_score': 0.8
            },
            {
                'title': '以太坊2.0合并进展顺利，开发者社区活跃',
                'content': '以太坊核心开发团队宣布2.0升级进展顺利，多个测试网已完成合并。社区开发者积极参与生态建设，DApp数量持续增长。',
                'source_name': '区块链日报',
                'source_url': 'https://blockchain-daily.com',
                'source_type': 'news', 
                'original_url': 'https://blockchain-daily.com/news/2001',
                'category': 'article',
                'tags': ['以太坊', '技术'],
                'publish_time': datetime.now(),
                'sentiment_score': 0.65,
                'importance_score': 0.7
            }
        ]
        
        success_count = 0
        for article_data in test_articles:
            if self.save_to_database(article_data):
                success_count += 1
        
        print(f"{self.name} 完成，成功保存 {success_count} 篇文章")
        return success_count
