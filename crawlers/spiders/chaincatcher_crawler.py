from utils.base_crawler import BaseCrawler
from datetime import datetime
from bs4 import BeautifulSoup

class ChainCatcherCrawler(BaseCrawler):
    def __init__(self):
        super().__init__('链捕手', 'https://www.chaincatcher.com')
    
    def parse_homepage(self):
        """解析首页新闻"""
        html = self.fetch_page(self.base_url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        articles = []
        
        # 查找新闻链接
        news_links = soup.select('a[href*="/news/"], a[href*="/article/"]')
        print(f"找到 {len(news_links)} 个新闻链接")
        
        processed_titles = set()  # 避免重复标题
        
        for link in news_links[:10]:  # 只取前10个
            try:
                title = link.get_text().strip()
                href = link.get('href', '')
                
                # 清理标题
                title = ' '.join(title.split())  # 移除多余空白
                
                if (title and len(title) > 15 and href and 
                    title not in processed_titles and
                    not title.startswith('快讯') and  # 过滤快讯
                    not title.startswith('数据：')):  # 过滤数据
                    
                    processed_titles.add(title)
                    
                    # 处理URL
                    if not href.startswith('http'):
                        href = self.base_url + href
                    
                    # 生成唯一标识
                    import hashlib
                    url_hash = hashlib.md5((title + href).encode()).hexdigest()[:8]
                    
                    article_data = {
                        'title': f"{title} [{url_hash}]",
                        'content': f"来自链捕手: {title}。这是链捕手提供的区块链行业新闻和分析报道。",
                        'summary': f"链捕手: {title}",
                        'source_name': self.name,
                        'source_url': self.base_url,
                        'source_type': 'news',
                        'original_url': href + f"?ref={url_hash}",
                        'category': 'article',
                        'tags': ['链捕手', '区块链'],
                        'publish_time': datetime.now(),
                        'importance_score': 0.8
                    }
                    articles.append(article_data)
                    print(f"准备保存: {title[:40]}...")
                    
            except Exception as e:
                print(f"解析链接失败: {e}")
                continue
        
        return articles  

    def run(self):
        """运行爬虫"""
        print(f"开始抓取 {self.name}...")
        
        articles = self.parse_homepage()
        success_count = 0
        
        for article in articles:
            if self.save_to_database(article):
                success_count += 1
                print(f"✅ 保存: {article['title'][:30]}...")
        
        print(f"{self.name} 抓取完成，成功保存 {success_count} 篇文章")
        return success_count
