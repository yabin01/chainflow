import React, { useState } from 'react';
import { Input, Select, Button, Space, Row, Col } from 'antd';
import { SearchOutlined } from '@ant-design/icons';

const { Search } = Input;
const { Option } = Select;

const SearchBar = ({ onSearch, loading }) => {
  const [searchText, setSearchText] = useState('');
  const [category, setCategory] = useState('');
  const [source, setSource] = useState('');

  const handleSearch = () => {
    onSearch({
      q: searchText,
      category: category || undefined,
      source: source || undefined,
    });
  };

  const handleReset = () => {
    setSearchText('');
    setCategory('');
    setSource('');
    onSearch({});
  };

  return (
    <div style={{ marginBottom: 20, padding: '20px', background: '#f5f5f5', borderRadius: 8 }}>
      <Row gutter={[16, 16]} align="middle">
        <Col xs={24} sm={12} md={8}>
          <Search
            placeholder="搜索文章标题、内容..."
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            onSearch={handleSearch}
            enterButton={<SearchOutlined />}
            size="large"
          />
        </Col>
        
        <Col xs={12} sm={6} md={4}>
          <Select
            placeholder="分类"
            value={category}
            onChange={setCategory}
            style={{ width: '100%' }}
            size="large"
            allowClear
          >
            <Option value="flash">快讯</Option>
            <Option value="article">文章</Option>
            <Option value="report">研报</Option>
            <Option value="announcement">公告</Option>
            <Option value="market">行情</Option>
          </Select>
        </Col>
        
        <Col xs={12} sm={6} md={4}>
          <Select
            placeholder="来源"
            value={source}
            onChange={setSource}
            style={{ width: '100%' }}
            size="large"
            allowClear
          >
            <Option value="金色财经">金色财经</Option>
            <Option value="币世界">币世界</Option>
            <Option value="PANews">PANews</Option>
          </Select>
        </Col>
        
        <Col xs={24} sm={12} md={8}>
          <Space>
            <Button type="primary" onClick={handleSearch} loading={loading} size="large">
              搜索
            </Button>
            <Button onClick={handleReset} size="large">
              重置
            </Button>
          </Space>
        </Col>
      </Row>
    </div>
  );
};

export default SearchBar;
