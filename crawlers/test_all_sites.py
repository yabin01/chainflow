#!/usr/bin/env python
"""
测试所有区块链新闻网站的可访问性
"""

import requests
import time
from datetime import datetime

def test_site(site_name, url, timeout=10):
    """测试单个网站的可访问性"""
    print(f"测试 {site_name}...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        response_time = round((time.time() - start_time) * 1000, 2)
        
        if response.status_code == 200:
            print(f"  ✅ 可访问 - 状态码: {response.status_code}, 响应时间: {response_time}ms")
            return True, response_time, len(response.text)
        else:
            print(f"  ⚠️  受限访问 - 状态码: {response.status_code}, 响应时间: {response_time}ms")
            return False, response_time, 0
            
    except requests.exceptions.Timeout:
        print(f"  ❌ 连接超时 (>{timeout}s)")
        return False, 0, 0
    except requests.exceptions.ConnectionError:
        print(f"  ❌ 连接失败")
        return False, 0, 0
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return False, 0, 0

def main():
    print("🌐 区块链新闻网站可访问性测试")
    print("=" * 50)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 要测试的网站列表
    sites = [
        ("Foresight News", "https://foresightnews.pro"),
        ("链捕手 ChainCatcher", "https://www.chaincatcher.com"),
        ("TechFlow", "https://techflowpost.com"),
        ("Odaily", "https://www.odaily.news"),
        ("律动 BlockBeats", "https://www.theblockbeats.info"),
        ("PANews", "https://www.panewslab.com"),
        ("Decrypt", "https://decrypt.co"),
        ("CoinAnk", "https://coinank.com"),
        ("金色财经", "https://www.jinse.com"),
        ("币世界", "https://www.bishijie.com")
    ]
    
    results = []
    accessible_count = 0
    
    for site_name, url in sites:
        accessible, response_time, content_length = test_site(site_name, url)
        results.append((site_name, url, accessible, response_time))
        
        if accessible:
            accessible_count += 1
        
        time.sleep(1)  # 避免请求过于频繁
    
    # 输出总结
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    print(f"总测试网站: {len(sites)}")
    print(f"可访问网站: {accessible_count}")
    print(f"成功率: {accessible_count/len(sites)*100:.1f}%")
    
    print("\n✅ 可访问的网站:")
    for site_name, url, accessible, response_time in results:
        if accessible:
            print(f"  - {site_name}: {response_time}ms")
    
    print("\n❌ 不可访问的网站:")
    for site_name, url, accessible, response_time in results:
        if not accessible:
            print(f"  - {site_name}")

if __name__ == "__main__":
    main()
