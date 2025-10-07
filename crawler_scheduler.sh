#!/bin/bash

# ChainFlow 爬虫定时任务管理脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_JOB="0 */2 * * * cd $SCRIPT_DIR/crawlers && $SCRIPT_DIR/backend/venv/bin/python crawler_manager.py >> $SCRIPT_DIR/crawlers/cron.log 2>&1"

case "$1" in
    install)
        echo "安装 ChainFlow 定时任务..."
        (crontab -l 2>/dev/null | grep -v "crawler_manager.py"; echo "$CRON_JOB") | crontab -
        echo "✅ 定时任务安装完成"
        echo "运行: crontab -l 查看任务"
        ;;
    uninstall)
        echo "卸载 ChainFlow 定时任务..."
        crontab -l 2>/dev/null | grep -v "crawler_manager.py" | crontab -
        echo "✅ 定时任务已卸载"
        ;;
    status)
        echo "当前定时任务:"
        crontab -l | grep -E "(crawler_manager.py|ChainFlow)" || echo "未找到相关任务"
        ;;
    run-now)
        echo "立即运行爬虫..."
        cd $SCRIPT_DIR/crawlers
        $SCRIPT_DIR/backend/venv/bin/python crawler_manager.py
        ;;
    *)
        echo "使用方法: $0 {install|uninstall|status|run-now}"
        echo "  install    - 安装每2小时运行的定时任务"
        echo "  uninstall  - 卸载定时任务"
        echo "  status     - 查看任务状态"
        echo "  run-now    - 立即运行爬虫"
        ;;
esac
