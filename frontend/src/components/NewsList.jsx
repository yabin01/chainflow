import React, { useState, useEffect } from 'react';
import { List, Card, Tag, Spin, Empty, message } from 'antd';
import { newsAPI } from '../services/api';

const NewsList = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pagination, setPagination] = useState({});

  // 分类颜色映射
  const categoryColors = {
    flash: 'red',
    article: 'blue',
    report: 'orange',
    announcement: 'green',
    market: 'purple',
  };

  // 获取文章列表
  const fetchArticles = async (page = 1) => {
    try {
      setLoading(true);
      const response = await newsAPI.getArticles({ page });
      setArticles(response.data.results);
      setPagination({
        current: page,
        total: response.data.count,
        pageSize: 20,
      });
    } catch (error) {
      message.error('获取文章列表失败');
      console.error('Error fetching articles:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchArticles();
  }, []);

  // 处理分页变化
  const handlePageChange = (page) => {
    fetchArticles(page);
  };

  // 格式化时间
  const formatTime = (timeString) => {
    return new Date(timeString).toLocaleString('zh-CN');
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>区块链新闻</h2>
      
      <Spin spinning={loading}>
        <List
          itemLayout="vertical"
          size="large"
          pagination={{
            ...pagination,
            onChange: handlePageChange,
            showSizeChanger: false,
            showQuickJumper: true,
          }}
          dataSource={articles}
          renderItem={(article) => (
            <List.Item key={article.id}>
              <Card>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                  <div style={{ flex: 1 }}>
                    <h3 style={{ marginBottom: 8 }}>
                      <a 
                        href={article.original_url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        style={{ color: '#1890ff', textDecoration: 'none' }}
                      >
                        {article.title}
                      </a>
                    </h3>
                    
                    <div style={{ marginBottom: 12 }}>
                      <Tag color={categoryColors[article.category] || 'default'}>
                        {article.category}
                      </Tag>
                      <Tag>{article.source_name}</Tag>
                      {article.sentiment_score && (
                        <Tag color={article.sentiment_score > 0.5 ? 'green' : 'red'}>
                          情感: {(article.sentiment_score * 100).toFixed(0)}%
                        </Tag>
                      )}
                    </div>

                    {article.summary && (
                      <p style={{ color: '#666', lineHeight: 1.6 }}>
                        {article.summary}
                      </p>
                    )}

                    <div style={{ marginTop: 12, color: '#999', fontSize: 12 }}>
                      <span>发布时间: {formatTime(article.publish_time)}</span>
                      <span style={{ marginLeft: 16 }}>浏览: {article.view_count}</span>
                      <span style={{ marginLeft: 16 }}>点赞: {article.like_count}</span>
                    </div>
                  </div>
                </div>
              </Card>
            </List.Item>
          )}
          locale={{
            emptyText: loading ? <Spin size="large" /> : <Empty description="暂无数据" />
          }}
        />
      </Spin>
    </div>
  );
};

export default NewsList;
