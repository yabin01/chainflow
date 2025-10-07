#!/bin/bash

echo "=== 启动ChainFlow后端服务 ==="

cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖（如果需要）
if [ ! -f ".deps-installed" ]; then
    echo "安装Python依赖..."
    pip install -r requirements.txt
    touch .deps-installed
fi

# 检查数据库迁移
echo "检查数据库..."
python manage.py migrate

echo ""
echo "启动Django开发服务器..."
echo "访问地址: http://localhost:8000"
echo "管理后台: http://localhost:8000/admin"
echo "按 Ctrl+C 停止服务器"
echo ""

python manage.py runserver 0.0.0.0:8000
