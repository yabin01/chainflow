from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chainflow_backend.news import views

# 创建路由器并注册视图集
router = DefaultRouter()
router.register(r'sources', views.NewsSourceViewSet)
router.register(r'articles', views.ArticleViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # API认证
]
