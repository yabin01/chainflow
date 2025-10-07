#!/bin/bash

echo "=== 第四步：数据爬虫完成检查 ==="

cd crawlers

echo "1. 检查爬虫文件..."
files=("utils/base_crawler.py" "spiders/jinse_crawler.py" "crawler_manager.py" "requirements.txt")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "✗ $file 缺失"
    fi
done

echo ""
echo "2. 检查依赖..."
if python -c "import requests, bs4, schedule" 2>/dev/null; then
    echo "✓ 爬虫依赖已安装"
else
    echo "✗ 爬虫依赖缺失"
fi
echo ""
echo "3. 测试爬虫..."
cd ~/chainflow/crawlers
python crawler_manager.py

echo ""
echo "✓ 第四步完成！"
echo "下一步：完善系统功能或部署上线"
