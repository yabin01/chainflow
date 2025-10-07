import time
import schedule
from spiders.foresight_crawler import ForesightNewsCrawler
from spiders.chaincatcher_crawler import ChainCatcherCrawler
from spiders.mock_crawler import MockCrawler

class CrawlerManager:
    def __init__(self, use_real=True):
        if use_real:
            self.crawlers = [
                ForesightNewsCrawler(),
                ChainCatcherCrawler(),
                # 可以继续添加其他真实爬虫
            ]
        else:
            self.crawlers = [MockCrawler()]
    
    def run_all(self):
        """运行所有爬虫"""
        print("🚀 开始运行所有爬虫...")
        total_success = 0
        
        for crawler in self.crawlers:
            try:
                print(f"\n=== 运行 {crawler.name} ===")
                success_count = crawler.run()
                total_success += success_count
                print(f"=== {crawler.name} 完成，保存 {success_count} 篇文章 ===\n")
                time.sleep(2)  # 避免请求过于频繁
            except Exception as e:
                print(f"❌ 爬虫 {crawler.name} 运行失败: {e}")
        
        print(f"🎉 所有爬虫运行完成，总共保存 {total_success} 篇文章")
        return total_success

if __name__ == "__main__":
    manager = CrawlerManager(use_real=True)
    manager.run_all()
