import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
from utils.base_crawler import BaseCrawler

class JinseCrawler(BaseCrawler):
    def __init__(self):
        super().__init__('金色财经', 'https://www.jinse.com')
    
    def parse_news_list(self):
        """解析新闻列表"""
        url = f"{self.base_url}/lives"
        html = self.fetch_page(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        articles = []
        
        # 解析快讯列表
        news_items = soup.select('.js-lives__item')
        for item in news_items[:20]:  # 限制数量避免过多
            try:
                title_elem = item.select_one('.js-lives__title')
                time_elem = item.select_one('.js-lives__time')
                content_elem = item.select_one('.js-lives__text')
                
                if not title_elem or not content_elem:
                    continue
                
                title = title_elem.get_text().strip()
                content = content_elem.get_text().strip()
                time_str = time_elem.get_text().strip() if time_elem else datetime.now().strftime('%H:%M')
                
                # 构建完整URL
                link_elem = item.select_one('a')
                article_url = self.base_url + link_elem['href'] if link_elem and link_elem.get('href') else ''
                
                # 处理时间
                publish_time = self.parse_time(f"{datetime.now().strftime('%Y-%m-%d')} {time_str}")
                
                article_data = {
                    'title': title,
                    'content': content,
                    'summary': content[:100] + '...' if len(content) > 100 else content,
                    'source_name': self.name,
                    'source_url': self.base_url,
                    'source_type': 'news',
                    'original_url': article_url,
                    'category': 'flash',
                    'publish_time': publish_time,
                    'importance_score': 0.6
                }
                
                articles.append(article_data)
                
            except Exception as e:
                print(f"解析金色财经项目失败: {e}")
                continue
        
        return articles
    
    def run(self):
        """运行爬虫"""
        print(f"开始爬取 {self.name}...")
        articles = self.parse_news_list()
        
        success_count = 0
        for article in articles:
            if self.save_to_database(article):
                success_count += 1
        
        print(f"{self.name} 爬取完成，成功保存 {success_count} 篇文章")
        return success_count
