#!/bin/bash

cd ~/chainflow

echo "=== 本地文件系统 ==="
ls -la

echo ""
echo "=== Git跟踪的文件 ==="
git ls-files

echo ""
echo "=== 提交历史 ==="
git log --oneline

echo ""
echo "=== 检查GitHub实际内容 ==="
cd /tmp
rm -rf check-gh
git clone https://github.com/yabin01/chainflow.git check-gh 2>/dev/null
if [ $? -eq 0 ]; then
    cd check-gh
    echo "GitHub仓库内容:"
    ls -la
    echo ""
    echo "文件总数: $(find . -type f -not -path "./.git/*" | wc -l)"
else
    echo "无法克隆仓库，可能认证问题"
fi
