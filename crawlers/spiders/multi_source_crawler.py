from utils.base_crawler import BaseCrawler
from datetime import datetime
import time
import random

class MultiSourceCrawler(BaseCrawler):
    def __init__(self):
        super().__init__('多源爬虫测试', 'https://multi.chainflow.com')
        
        # 定义要测试的网站列表
        self.websites = [
            {
                'name': 'Foresight News',
                'url': 'https://foresightnews.pro',
                'test_url': 'https://foresightnews.pro/article/list',
                'type': 'news'
            },
            {
                'name': '链捕手 ChainCatcher',
                'url': 'https://www.chaincatcher.com',
                'test_url': 'https://www.chaincatcher.com/',
                'type': 'news'
            },
            {
                'name': 'TechFlow',
                'url': 'https://techflowpost.com',
                'test_url': 'https://techflowpost.com/',
                'type': 'news'
            },
            {
                'name': 'Odaily',
                'url': 'https://www.odaily.news',
                'test_url': 'https://www.odaily.news/',
                'type': 'news'
            },
            {
                'name': '律动 BlockBeats',
                'url': 'https://www.theblockbeats.info',
                'test_url': 'https://www.theblockbeats.info/',
                'type': 'news'
            },
            {
                'name': 'PANews',
                'url': 'https://www.panewslab.com',
                'test_url': 'https://www.panewslab.com/zh/index.html',
                'type': 'news'
            },
            {
                'name': 'Decrypt',
                'url': 'https://decrypt.co',
                'test_url': 'https://decrypt.co/',
                'type': 'news'
            },
            {
                'name': 'CoinAnk',
                'url': 'https://coinank.com',
                'test_url': 'https://coinank.com/',
                'type': 'news'
            }
        ]

    def test_website_accessibility(self, website):
        """测试网站可访问性"""
        print(f"🔍 测试 {website['name']} ({website['test_url']})...")
        
        try:
            start_time = time.time()
            html_content = self.fetch_page(website['test_url'], timeout=15)
            response_time = round((time.time() - start_time) * 1000, 2)
            
            if html_content:
                # 简单分析页面内容
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                title = soup.title.string if soup.title else "无标题"
                print(f"   ✅ 连接成功 - 响应时间: {response_time}ms")
                print(f"      页面标题: {title[:50]}...")
                print(f"      内容长度: {len(html_content)} 字符")
                return True, response_time, len(html_content)
            else:
                print(f"   ❌ 连接失败 - 无法获取内容")
                return False, response_time, 0
                
        except Exception as e:
            print(f"   ❌ 连接异常: {e}")
            return False, 0, 0

    def parse_simple_news(self, website, html_content):
        """简单解析新闻内容（基础版本）"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 尝试提取标题和链接（通用选择器）
            articles = []
            
            # 常见的选择器模式
            selectors = [
                'a[href*="article"]', 
                'a[href*="news"]',
                '.title a',
                '.news-item a',
                'h2 a',
                'h3 a'
            ]
            
            for selector in selectors:
                links = soup.select(selector)
                if links:
                    for link in links[:3]:  # 只取前3个
                        title = link.get_text().strip()
                        href = link.get('href', '')
                        
                        if title and len(title) > 10:
                            # 处理相对URL
                            if href.startswith('/'):
                                href = website['url'] + href
                            elif not href.startswith('http'):
                                href = website['url'] + '/' + href
                            
                            articles.append({
                                'title': title,
                                'url': href,
                                'source': website['name']
                            })
                    break
            
            return articles
            
        except Exception as e:
            print(f"   解析失败: {e}")
            return []

    def run_accessibility_test(self):
        """运行网站可访问性测试"""
        print("🌐 开始测试区块链新闻网站可访问性...")
        print("=" * 60)
        
        results = []
        accessible_sites = []
        
        for website in self.websites:
            success, response_time, content_length = self.test_website_accessibility(website)
            
            results.append({
                'name': website['name'],
                'url': website['url'],
                'accessible': success,
                'response_time': response_time,
                'content_length': content_length
            })
            
            if success:
                accessible_sites.append(website['name'])
            
            # 添加随机延迟，避免请求过于频繁
            time.sleep(random.uniform(1, 3))
        
        # 输出测试结果摘要
        print("\n" + "=" * 60)
        print("📊 可访问性测试结果摘要:")
        print(f"   总测试网站: {len(self.websites)}")
        print(f"   可访问网站: {len(accessible_sites)}")
        print(f"   成功率: {len(accessible_sites)/len(self.websites)*100:.1f}%")
        
        if accessible_sites:
            print("   ✅ 可访问的网站:")
            for site in accessible_sites:
                print(f"      - {site}")
        
        inaccessible = [r['name'] for r in results if not r['accessible']]
        if inaccessible:
            print("   ❌ 不可访问的网站:")
            for site in inaccessible:
                print(f"      - {site}")
        
        return results, accessible_sites

    def try_crawl_accessible_sites(self, accessible_sites):
        """尝试抓取可访问的网站"""
        print("\n🕷️ 尝试抓取可访问网站的新闻...")
        
        crawled_articles = 0
        for website_info in self.websites:
            if website_info['name'] in accessible_sites:
                print(f"\n📰 尝试抓取 {website_info['name']}...")
                
                try:
                    html_content = self.fetch_page(website_info['test_url'], timeout=15)
                    if html_content:
                        articles = self.parse_simple_news(website_info, html_content)
                        
                        if articles:
                            print(f"   发现 {len(articles)} 篇文章")
                            
                            # 保存到数据库
                            for article in articles[:2]:  # 只保存前2篇测试
                                article_data = {
                                    'title': article['title'],
                                    'content': f"来自 {website_info['name']} 的新闻: {article['title']}",
                                    'summary': f"来自 {website_info['name']}: {article['title']}",
                                    'source_name': website_info['name'],
                                    'source_url': website_info['url'],
                                    'source_type': 'news',
                                    'original_url': article['url'],
                                    'category': 'article',
                                    'tags': [website_info['name'], '区块链'],
                                    'publish_time': datetime.now(),
                                    'importance_score': 0.7
                                }
                                
                                if self.save_to_database(article_data):
                                    crawled_articles += 1
                                    print(f"   ✅ 保存: {article['title'][:30]}...")
                        else:
                            print("   未找到可解析的文章")
                    else:
                        print("   无法获取页面内容")
                        
                except Exception as e:
                    print(f"   抓取失败: {e}")
                
                # 添加延迟
                time.sleep(2)
        
        return crawled_articles

    def run(self):
        """运行多源爬虫测试"""
        print("🚀 启动多源区块链新闻爬虫测试")
        
        # 健康检查
        health = self.health_check()
        print(f"📊 爬虫健康状态: {health}")
        
        # 测试网站可访问性
        results, accessible_sites = self.run_accessibility_test()
        
        # 如果有关可访问的网站，尝试抓取
        if accessible_sites:
            crawled_count = self.try_crawl_accessible_sites(accessible_sites)
            print(f"\n🎉 抓取完成，成功保存 {crawched_count} 篇文章")
            return crawled_count
        else:
            print("\n😞 没有可访问的网站，无法抓取数据")
            return 0
