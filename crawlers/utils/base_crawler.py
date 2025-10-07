import requests
import time
import logging
from datetime import datetime
from bs4 import BeautifulSoup
import os
import sys
import django

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BaseCrawler:
    def __init__(self, name, base_url):
        self.name = name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # 初始化Django环境
        self._setup_django()
    
    def _setup_django(self):
        """设置Django环境"""
        try:
            # 添加backend到Python路径
            backend_path = os.path.join(os.path.dirname(__file__), '../../backend')
            if backend_path not in sys.path:
                sys.path.append(backend_path)
            
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chainflow_backend.settings')
            django.setup()
            logger.info("Django环境设置成功")
        except Exception as e:
            logger.error(f"Django环境设置失败: {e}")
            raise
    
    def fetch_page(self, url, method='GET', data=None, retries=3, timeout=10):
        """获取页面内容（带重试机制）"""
        for attempt in range(retries):
            try:
                logger.info(f"请求页面: {url} (尝试 {attempt + 1}/{retries})")
                
                if method.upper() == 'GET':
                    response = self.session.get(url, timeout=timeout)
                else:
                    response = self.session.post(url, data=data, timeout=timeout)
                
                response.raise_for_status()
                
                # 自动检测编码
                if response.encoding is None:
                    response.encoding = 'utf-8'
                
                logger.info(f"页面获取成功: {url} (状态码: {response.status_code})")
                return response.text
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"请求失败 {url} (尝试 {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    wait_time = 2 ** attempt  # 指数退避
                    logger.info(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"所有重试失败: {url}")
                    return None
            except Exception as e:
                logger.error(f"未知错误: {url} - {e}")
                return None
    
    def parse_time(self, time_str, default=None):
        """解析时间字符串"""
        if not time_str:
            return default or datetime.now()
        
        try:
            # 移除多余空格
            time_str = time_str.strip()
            
            # 常见时间格式
            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y/%m/%d %H:%M:%S',
                '%Y-%m-%dT%H:%M:%S',
                '%Y年%m月%d日 %H:%M',
                '%m-%d %H:%M',
                '%H:%M',
                '%Y-%m-%d',
                '%Y/%m/%d'
            ]
            
            for fmt in formats:
                try:
                    parsed_time = datetime.strptime(time_str, fmt)
                    # 如果年份缺失，使用当前年份
                    if parsed_time.year == 1900:
                        parsed_time = parsed_time.replace(year=datetime.now().year)
                # 添加时区信息
                    from django.utils import timezone
                    if timezone.is_naive(parsed_time):
                        parsed_time = timezone.make_aware(parsed_time)

                    return parsed_time
                except ValueError:
                    continue
            
            logger.warning(f"无法解析时间格式: {time_str}")
            return default or datetime.now()
            
        except Exception as e:
            logger.warning(f"时间解析失败 {time_str}: {e}")
            return default or datetime.now()
    
    def clean_content(self, content):
        """清理内容文本"""
        if not content:
            return ""
        
        try:
            # 移除HTML标签
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text()
            
            # 清理空白字符
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            cleaned_text = ' '.join(lines)
            
            # 移除常见广告文本
            ads_keywords = ['广告', '推广', '免责声明', '风险提示', '点击查看']
            for keyword in ads_keywords:
                if keyword in cleaned_text:
                    cleaned_text = cleaned_text.split(keyword)[0].strip()
            
            return cleaned_text
            
        except Exception as e:
            logger.warning(f"内容清理失败: {e}")
            return content.strip() if content else ""
    
    def extract_summary(self, content, max_length=150):
        """从内容中提取摘要"""
        if not content:
            return ""
        
        cleaned_content = self.clean_content(content)
        
        if len(cleaned_content) <= max_length:
            return cleaned_content
        
        # 尝试在句子边界截断
        summary = cleaned_content[:max_length]
        last_period = summary.rfind('。')
        last_exclamation = summary.rfind('！')
        last_question = summary.rfind('？')
        
        cut_pos = max(last_period, last_exclamation, last_question)
        if cut_pos > max_length * 0.5:  # 确保不会截断太早
            summary = summary[:cut_pos + 1]
        
        return summary + '...'
    
    def save_to_database(self, article_data):
        """保存文章到数据库"""
        try:
            from chainflow_backend.news.models import NewsSource, Article
            from django.utils import timezone
            
            # 获取或创建新闻来源
            source, created = NewsSource.objects.get_or_create(
                name=article_data['source_name'],
                defaults={
                    'url': article_data.get('source_url', ''),
                    'type': article_data.get('source_type', 'news')
                }
            )
            
            if created:
                logger.info(f"创建新来源: {source.name}")
            
            # 检查文章是否已存在（基于URL）
            if Article.objects.filter(original_url=article_data['original_url']).exists():
                logger.info(f"文章已存在，跳过: {article_data['title']}")
                return False
            
            # 创建文章
            article = Article(
                title=article_data['title'],
                content=article_data['content'],
                summary=article_data.get('summary', ''),
                source=source,
                original_url=article_data['original_url'],
                category=article_data.get('category', 'article'),
                tags=article_data.get('tags', []),
                publish_time=article_data.get('publish_time', timezone.now()),
                sentiment_score=article_data.get('sentiment_score'),
                importance_score=article_data.get('importance_score', 0.5)
            )
            
            # 自动生成摘要（如果未提供）
            if not article.summary and article.content:
                article.summary = self.extract_summary(article.content)
            
            article.save()
            
            logger.info(f"✅ 保存文章成功: {article.title}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 保存到数据库失败: {e}")
            return False
    
    def run(self):
        """运行爬虫（子类必须实现）"""
        raise NotImplementedError("子类必须实现 run() 方法")
    
    def health_check(self):
        """健康检查"""
        try:
            # 测试网络连接
            test_response = self.session.get('https://httpbin.org/get', timeout=5)
            network_ok = test_response.status_code == 200
            
            # 测试数据库连接
            from chainflow_backend.news.models import NewsSource
            db_ok = NewsSource.objects.exists() or True  # 即使为空表也认为正常
            
            return {
                'network': network_ok,
                'database': db_ok,
                'crawler': True
            }
            
        except Exception as e:
            logger.error(f"健康检查失败: {e}")
            return {
                'network': False,
                'database': False,
                'crawler': False
            }
