import React, { useState, useEffect } from 'react';
import { Layout, Typography, message } from 'antd';
import NewsList from './components/NewsList';
import SearchBar from './components/SearchBar';
import { newsAPI } from './services/api';
import './App.css';

const { Header, Content } = Layout;
const { Title } = Typography;

function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchParams, setSearchParams] = useState({});

  // 获取文章数据
  const fetchArticles = async (params = {}) => {
    try {
      setLoading(true);
      let response;
      
      if (params.q) {
        // 使用搜索API
        response = await newsAPI.searchArticles(params.q, params);
      } else {
        // 使用普通文章列表API
        response = await newsAPI.getArticles(params);
      }
      
      setArticles(response.data.results || []);
    } catch (error) {
      message.error('获取数据失败');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  // 处理搜索
  const handleSearch = (params = {}) => {
    setSearchParams(params);
    fetchArticles(params);
  };

  // 初始加载
  useEffect(() => {
    fetchArticles();
  }, []);

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ 
        background: '#001529', 
        display: 'flex', 
        alignItems: 'center',
        padding: '0 24px'
      }}>
        <Title level={3} style={{ color: 'white', margin: 0 }}>
          🔗 ChainFlow - 区块链信息流
        </Title>
      </Header>
      
      <Content style={{ padding: '0 24px', background: '#fff' }}>
        <div style={{ maxWidth: 1200, margin: '0 auto' }}>
          <SearchBar onSearch={handleSearch} loading={loading} />
          <NewsList 
            articles={articles}
            loading={loading}
            onRefresh={() => fetchArticles(searchParams)}
          />
        </div>
      </Content>
    </Layout>
  );
}

export default App;
