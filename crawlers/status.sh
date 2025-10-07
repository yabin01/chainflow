#!/bin/bash

echo "=== ChainFlow 系统状态 ==="

# 检查后端
echo "后端服务:"
curl -s http://localhost:8000/api/articles/ > /dev/null
if [ $? -eq 0 ]; then
    count=$(curl -s http://localhost:8000/api/articles/ | python3 -c "import sys, json; print(json.load(sys.stdin)['count'])")
    echo "✅ 运行正常 (文章: $count 篇)"
else
    echo "❌ 未运行"
fi

# 检查前端
echo "前端服务:"
curl -s http://localhost:3000 > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ 运行正常"
else
    echo "❌ 未运行"
fi

# 检查数据
echo "数据状态:"
cd ~/chainflow/crawlers
python check_data.py
