#!/bin/bash

echo "=== 修复后端依赖 ==="

cd backend

# 安装系统依赖
echo "安装系统依赖..."
sudo apt update
sudo apt install -y python3-dev libpq-dev build-essential

# 创建虚拟环境
echo "设置Python虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 创建简化依赖文件
echo "安装Python包..."
cat > requirements-dev.txt << 'REQ'
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
beautifulsoup4==4.12.2
requests==2.31.0
python-dotenv==1.0.0
REQ

pip install --upgrade pip
pip install -r requirements-dev.txt

echo "✓ 依赖安装完成"
