import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log(`发起请求: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API请求错误:', error);
    return Promise.reject(error);
  }
);

// API方法
export const newsAPI = {
  // 获取文章列表
  getArticles: (params = {}) => api.get('/articles/', { params }),
  
  // 获取文章详情
  getArticle: (id) => api.get(`/articles/${id}/`),
  
  // 获取最新文章
  getLatestArticles: (limit = 10) => api.get(`/articles/latest/?limit=${limit}`),
  
  // 搜索文章
  searchArticles: (query, params = {}) => 
    api.get('/articles/search/', { params: { q: query, ...params } }),
  
  // 获取新闻来源
  getSources: () => api.get('/sources/'),
  
  // 增加文章浏览量
  incrementViewCount: (id) => api.post(`/articles/${id}/increment_view_count/`),
};

export default api;
