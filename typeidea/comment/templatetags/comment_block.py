from django import template

from comment.forms import CommentForm
from comment.models import Comment

register = template.Library()


@register.inclusion_tag("comment/comment_block.html")
def comment_block(request):
    """
        因为自定义的标签所用到的comment_block.html页面中，默认是没有request 对象的。
        所以需要手动将request通过context_data传递到了comment_block.html页面中引用，
        这也是为什么自定义标签函数通常第一个参数是request对象，return必须是一个字
        典（context_data），用于子模板的渲染。
    """
    return {
        "request": request,
        "comment_form": CommentForm(),
        "comment_list": Comment.get_comments_by_post_url(request.path),
    }
