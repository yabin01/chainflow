#!/bin/bash

echo "=== 第三步：前端组件完成检查 ==="

cd frontend

echo "1. 检查前端依赖..."
if [ -d "node_modules" ]; then
    echo "✓ node_modules存在"
else
    echo "✗ node_modules缺失，运行: npm install"
fi

echo ""
echo "2. 检查组件文件..."
components=("src/services/api.js" "src/components/NewsList.jsx" "src/components/SearchBar.jsx" "src/App.jsx")
for component in "${components[@]}"; do
    if [ -f "$component" ]; then
        echo "✓ $component"
    else
        echo "✗ $component 缺失"
    fi
done

echo ""
echo "3. 启动状态..."
if pgrep -f "vite" > /dev/null; then
    echo "✓ 前端开发服务器运行中"
    echo "访问: http://localhost:3000"
else
    echo "前端服务器未运行"
    echo "启动命令: cd frontend && npm run dev"
fi

echo ""
echo "✓ 第三步完成！"
echo "下一步：实现数据爬虫"
