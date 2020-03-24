from rest_framework import serializers, pagination
from rest_framework import generics

from .models import Post, Category, Tag


"""通过URL来标记资源相对于通过id标记更为合理"""
# 使用HyperlinkedIdentityField字段时，可以不继承自HyperlinkedModelSerializer
# class PostSerializer(serializers.HyperlinkedModelSerializer):
# 文章列表api
class PostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True
    )
    tag = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        read_only=True
    )
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # 这里的view_name就是urls中router的base_name+列表/详情页，因此在不定义namespace的前提条件
    # 下base_name从另一个层面实现了namespace。冒号前面的api为urls中定义的namespace
    url = serializers.HyperlinkedIdentityField(view_name="api:api-post-detail")

    class Meta:
        model = Post
        fields = ("url", "id", "title", "category", "tag", "owner", "created_time")


# 文章详情api
class PostDetailSerializer(PostSerializer):
    # 文章详情页需要多输出一个字段content_html
    class Meta:
        model = Post
        fields = ("url", "id", "title", "category", "tag", "owner", "content_html", "created_time")


# 另外一种方式是通过在Meta中定义extra_kwargs属性来指定url
# class CategorySerializer(serializers.HyperlinkedModelSerializer):
class CategorySerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Category
        fields = ("url", "id", "name", "created_time")
        extra_kwargs = {
            "url": {"view_name": "api:api-category-detail"}
        }


class CategoryDetailSerializer(CategorySerializer):
    posts = serializers.SerializerMethodField("paginated_posts")

    # obj为某一个category实例对象
    def paginated_posts(self, obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        # paginate_queryset要从request的查询字符串中获取page_size的值。
        page = paginator.paginate_queryset(posts, self.context["request"])
        # 由于序列化的是分页page数据，每一页的数据不同，所以需要从request的查询字符串中获取page_size的值。
        serializer = PostSerializer(page, many=True, context={"request": self.context["request"]})
        return {
            "count": posts.count(),
            "results": serializer.data,
            "previous": paginator.get_previous_link(),
            "next": paginator.get_next_link()
        }

    class Meta:
        model = Category
        fields = ("url", "id", "name", "created_time", "posts")
        extra_kwargs = {
            "url": {"view_name": "api:api-category-detail"}
        }


class TagSerializer(serializers.HyperlinkedModelSerializer):
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    url = serializers.HyperlinkedIdentityField(view_name="api:api-tag-detail")

    class Meta:
        model = Tag
        fields = ("url", "id", "name", "created_time")


class TagDetailSerializer(TagSerializer):
    posts = serializers.SerializerMethodField("paginated_posts")

    def paginated_posts(self, obj):
        posts = Post.objects.filter(tag=obj)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts, self.context["request"])
        serializer = PostSerializer(page, many=True, context={"request": self.context["request"]})
        return {
            "count": posts.count(),
            "results": serializer.data,
            "previous": paginator.get_previous_link(),
            "next": paginator.get_next_link(),
        }

    class Meta:
        model = Tag
        fields = ("url", "id", "name", "posts", "created_time")
