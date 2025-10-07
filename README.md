# 🔗 ChainFlow - 区块链信息聚合平台

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个现代化的区块链新闻和信息聚合平台，实时抓取和分析多个权威数据源的区块链资讯，为投资者和爱好者提供全面的市场洞察。

![ChainFlow Screenshot](https://via.placeholder.com/800x400/001529/FFFFFF?text=ChainFlow+Blockchain+News+Aggregator)

## ✨ 核心特性

### 📰 智能信息聚合
- **多源数据采集** - 集成 ChainCatcher、Foresight News 等权威数据源
- **实时内容更新** - 自动定时抓取最新区块链新闻和市场动态
- **智能去重算法** - 基于URL哈希的重复内容检测和过滤
- **内容分类系统** - 快讯、文章、研报、行情等多维度分类

### 🔍 高级搜索分析
- **全文搜索引擎** - 支持标题、内容、摘要的多字段搜索
- **智能筛选系统** - 按来源、分类、时间范围精准过滤
- **情感分析** - 自动分析文章情感倾向（积极/消极）
- **重要性评分** - 基于内容质量自动评估文章重要性

### 🎨 现代用户体验
- **响应式设计** - 完美适配桌面、平板和移动设备
- **直观界面** - 基于 Ant Design 的现代化UI组件
- **实时数据** - WebSocket 支持实时内容更新
- **个性化推荐** - 基于用户行为的智能内容推荐

### ⚙️ 企业级架构
- **微服务架构** - 前后端分离，支持独立部署和扩展
- **RESTful API** - 标准化接口设计，便于第三方集成
- **自动化运维** - 完整的CI/CD流水线和监控体系
- **高可用性** - 负载均衡和故障转移机制

## 🏗️ 系统架构

```mermaid
graph TB
    A[用户界面] --> B[前端服务]
    B --> C[API网关]
    C --> D[用户服务]
    C --> E[新闻服务]
    C --> F[搜索服务]
    
    G[爬虫集群] --> E
    H[数据源] --> G
    
    E --> I[(数据库)]
    F --> I
    D --> I
    
    subgraph "数据源"
        H1[ChainCatcher]
        H2[Foresight News]
        H3[PANews]
        H4[Odaily]
    end
    
    subgraph "爬虫系统"
        G1[调度器]
        G2[解析器]
        G3[去重器]
        G4[存储器]
    end

#📄 许可证
本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详情。

#🙏 致谢
感谢以下开源项目的支持：
Django - Python Web框架
React - 用户界面库
Ant Design - 企业级UI设计语言
Beautiful Soup - HTML解析库

#📞 联系我们
项目主页: https://github.com/yabin01/chainflow
问题反馈: GitHub Issues
邮箱联系: [yabinliu1997@gmail.com]

<div align="center">
如果这个项目对你有帮助，请给个 ⭐️ 支持一下！

</div> ```
