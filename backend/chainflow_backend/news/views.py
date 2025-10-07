from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import NewsSource, Article
from .serializers import (
    NewsSourceSerializer, 
    ArticleListSerializer, 
    ArticleDetailSerializer
)

class NewsSourceViewSet(viewsets.ModelViewSet):
    queryset = NewsSource.objects.filter(is_active=True)
    serializer_class = NewsSourceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type']
    search_fields = ['name']

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(is_active=True).select_related('source')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['source', 'category']
    search_fields = ['title', 'content', 'summary']
    ordering_fields = ['publish_time', 'view_count', 'like_count', 'importance_score']
    ordering = ['-publish_time']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleDetailSerializer
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """获取最新文章"""
        limit = request.query_params.get('limit', 10)
        try:
            limit = min(int(limit), 50)  # 限制最大数量
        except ValueError:
            limit = 10
            
        articles = self.get_queryset()[:limit]
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """高级搜索接口"""
        query = request.query_params.get('q', '')
        category = request.query_params.get('category', '')
        source = request.query_params.get('source', '')
        
        queryset = self.get_queryset()
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) |
                Q(summary__icontains=query)
            )
        
        if category:
            queryset = queryset.filter(category=category)
            
        if source:
            queryset = queryset.filter(source__name__icontains=source)
            
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def increment_view_count(self, request, pk=None):
        """增加文章浏览次数"""
        article = self.get_object()
        article.view_count += 1
        article.save()
        return Response({'view_count': article.view_count})
