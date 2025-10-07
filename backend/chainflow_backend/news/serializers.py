from rest_framework import serializers
from .models import NewsSource, Article

class NewsSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsSource
        fields = ['id', 'name', 'url', 'type', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

class ArticleListSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source='source.name', read_only=True)
    source_type = serializers.CharField(source='source.type', read_only=True)
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'summary', 'source_name', 'source_type', 
            'category', 'publish_time', 'view_count', 'like_count',
            'sentiment_score', 'importance_score'
        ]

class ArticleDetailSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source='source.name', read_only=True)
    source_url = serializers.CharField(source='source.url', read_only=True)
    
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
