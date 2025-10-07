#!/bin/bash

cd ~/chainflow

echo "=== 设置ChainFlow项目 ==="

# 创建基础文件
echo "创建基础项目文件..."

# 标记文件
touch backend/.gitkeep frontend/.gitkeep crawlers/.gitkeep docker/.gitkeep docs/.gitkeep scripts/.gitkeep

echo "✓ 项目结构创建完成"

# 添加文件到Git
echo "添加文件到Git..."
git add -A

echo "=== 当前状态 ==="
git status

echo ""
echo "执行以下命令完成提交:"
echo "git commit -m 'feat: create complete project structure'"
echo "git push origin main"
