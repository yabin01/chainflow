#!/bin/bash

echo "=== 启动ChainFlow开发环境 ==="

# 启动后端
echo "1. 启动后端服务..."
cd backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000 &

# 等待后端启动
sleep 3

# 启动前端
echo "2. 启动前端服务..."
cd ../frontend
npm run dev &

echo ""
echo "✓ 开发环境启动完成!"
echo "后端: http://localhost:8000"
echo "前端: http://localhost:3000"
echo "管理后台: http://localhost:8000/admin"
echo ""
echo "按 Ctrl+C 停止所有服务"
