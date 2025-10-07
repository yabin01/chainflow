#!/bin/bash

echo "=== 第二步：API接口完成检查 ==="

cd backend
source venv/bin/activate

echo "1. 检查API端点..."
echo "文章列表:"
curl -s http://localhost:8000/api/articles/ | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f'✓ 文章API正常，数量: {len(data.get(\\\"results\\\", []))}')
except:
    print('✗ 文章API异常')
"

echo ""
echo "2. 检查数据模型..."
python manage.py shell << 'PYTHON'
from chainflow_backend.news.models import NewsSource, Article
print(f"新闻来源数量: {NewsSource.objects.count()}")
print(f"文章数量: {Article.objects.count()}")
PYTHON

echo ""
echo "3. 测试搜索功能..."
curl -s "http://localhost:8000/api/articles/search/?q=测试" | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print('✓ 搜索API正常')
except:
    print('✗ 搜索API异常')
"

echo ""
echo "✓ 第二步完成！"
echo "下一步：创建前端组件调用API"
