"""
# 使用viewset代替
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer


@api_view(["GET"])
def post_list(request):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    post_serializers = PostSerializer(queryset, many=True)
    return Response(post_serializers.data)


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Post, Category, Tag
from .serializers import (
    PostSerializer, PostDetailSerializer,
    CategorySerializer, CategoryDetailSerializer,
    TagSerializer, TagDetailSerializer,
)


# class PostViewSet(viewsets.ReadOnlyModelViewSet):
class PostViewSet(viewsets.ModelViewSet):
    """接口集"""
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer
    # 只有admin user才能够访问该api viewset
    # permission_classes = IsAdminUser

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    # 获取某个分类下的所有文章，通过query string来过滤queryset
    def filter_queryset(self, queryset):
        """
            filter_queryset的缺点是则无法取到category的字段信息。
            即文章资源的获取与其所属分类数据的获取是割裂的。
        """
        catetory_id = self.request.query_params.get("category")
        if catetory_id:
            queryset = queryset.filter(category__id=catetory_id)
        return queryset


# 通过CategoryDetailSerializer获取某个分类下的所有文章
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        """post文章的获取与其所属category分类的数据都可以取回来"""
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.filter(status=Tag.STATUS_NORMAL)
    serializer_class = TagSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = TagDetailSerializer
        return super().retrieve(request, *args, **kwargs)
