#!/bin/bash

echo "=== 检查GitHub远程仓库 ==="

cd ~/chainflow

echo "1. 本地提交历史:"
git log --oneline -5

echo ""
echo "2. 本地文件:"
find . -type f -not -path "./.git/*" | wc -l

echo ""
echo "3. 检查远程仓库..."
cd /tmp
rm -rf check-remote
if git clone https://github.com/yabin01/chainflow.git check-remote 2>/dev/null; then
    cd check-remote
    echo "✓ 成功克隆远程仓库"
    echo "远程仓库文件:"
    find . -type f -not -path "./.git/*" | wc -l
    echo ""
    echo "目录结构:"
    ls -la
else
    echo "✗ 无法克隆仓库"
fi
