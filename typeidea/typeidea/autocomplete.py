from dal import autocomplete

from blog.models import Category, Tag


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    # get_queryset的输入就是self.q，输出就是queryset,所以可以根据输入关键字来调用搜索接口，最终封装为QuerySet对象
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            queryset = Category.objects.none()
            # 直接返回空的queryset，因为最后结果还会被其他模块处理，所以不能直接返回None
            return queryset

        queryset = Category.objects.filter(owner=self.request.user)

        # self.q为url中查询字符串的value
        if self.q:
            queryset = queryset.filter(name__istartswith=self.q)
        return queryset


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            queryset = Tag.objects.none()
            return queryset

        queryset = Tag.objects.filter(owner=self.request.user)

        if self.q:
            queryset = queryset.filter(name__istartswith=self.q)
        return queryset
