#!/bin/bash

echo "=== ChainFlow开发环境状态 ==="
echo ""

# 检查后端
echo "🔧 后端服务:"
if curl -s http://localhost:8000/api/articles/ > /dev/null; then
    echo "   ✅ 运行正常 (http://localhost:8000)"
    # 获取文章数量
    count=$(curl -s http://localhost:8000/api/articles/ | python3 -c "import sys, json; print(json.load(sys.stdin)['count'])")
    echo "   文章数量: $count"
else
    echo "   ❌ 未运行"
fi

echo ""

# 检查前端
echo "🎨 前端服务:"
if curl -s http://localhost:3000 > /dev/null; then
    echo "   ✅ 运行正常 (http://localhost:3000)"
else
    echo "   ❌ 未运行"
fi

echo ""
echo "📊 服务状态:"
echo "   后端API: http://localhost:8000/api/articles/"
echo "   前端应用: http://localhost:3000"
echo "   管理后台: http://localhost:8000/admin"
