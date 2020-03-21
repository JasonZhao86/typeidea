from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import CommentForm


class CommentView(TemplateView):
    http_method_names = ["post"]
    template_name = "comment/result.html"

    def post(self, request, *args, **kwargs):
        form_data = CommentForm(request.POST)
        target = request.POST.get("target")

        if form_data.is_valid():
            comment = form_data.save(commit=False)
            comment.target = target
            comment.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False

        context = {
            "success": succeed,
            "target": target,
            "form_data": form_data,
        }
        return self.render_to_response(context)
