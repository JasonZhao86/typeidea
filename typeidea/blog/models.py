import mistune

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    ]

    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "分类"

    def __str__(self):
        return "<Category: {}>".format(self.name)

    @classmethod
    def get_nav(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        """
        # 两次数据库I/O请求，因为queryset是懒加载模式，返回的其实是一个查询，并不是真正被查询后的数据
        nav_categories = categories.filter(is_nav=True)
        normal_categories = categories.filter(is_nav=False)
        return {"nav_categories": nav_categories, "normal_categories": normal_categories}
        """
        nav_categories = []
        normal_categories = []
        for category in categories:   # 只有一次数据库I/O，返回的是从数据库中查询出来的真正的数据
            if category.is_nav:
                nav_categories.append(category)
            else:
                normal_categories.append(category)
        return {"nav_categories": nav_categories, "normal_categories": normal_categories}


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    ]

    name = models.CharField(max_length=10, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "标签"

    def __str__(self):
        return "<Tag: {}>".format(self.name)


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = [
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
        (STATUS_DRAFT, "草稿"),
    ]

    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    content = models.TextField(verbose_name="正文", help_text="正文必须为MarkDown格式")
    content_html = models.TextField(verbose_name="mistune转码后的html正文", blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    category = models.ForeignKey(Category, verbose_name="分类")
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ["-id"]

    def __str__(self):
        return "<Post: {}>".format(self.title)

    # save方法有很多参数，这里为了简洁，直接使用*args和**kwargs代替
    def save(self, *args, **kwargs):
        """
            在Post中增加content_html字段存储mistune转码后的html内容是考虑到文章的内容需要经常修改，
            如果文章保存时在post的AdminForm中直接将mistune转码后的html代码存储到content字段，而后
            作者再次修改文章内容时返回的是转码后的html代码，而不是markdown格式的代码，这显然不合适，
            因此增加content_html字段是为了显示用，原先的content字段是为了写入post文章时展示为编辑者
            用的。
        """
        self.content_html = mistune.markdown(self.content)
        super(Post, self).save(*args, **kwargs)

    @staticmethod
    def get_post_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related("owner", "category")
        return tag, post_list

    @staticmethod
    def get_post_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related("owner", "category")
        return category, post_list

    @classmethod
    def get_lastest_post(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).select_related("owner", "category")

    @classmethod
    def get_post_by_id(cls, post_id):
        try:
            post = cls.objects.get(id=post_id)
        except cls.DoesNotExist:
            post = None
        return post

    @classmethod
    def get_hot_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by("-pv")
