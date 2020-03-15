from django.http import JsonResponse
from django.views.generic import View
from .models import Comment
from django.core.urlresolvers import reverse
# Create your views here.


class CommentView(View):
    """
    处理评论
    """
    ret_msg = {"status": 0, "msg": {}}

    def post(self, request, *args, **kwargs):
        if not request.user.username:
            self.ret_msg['msg']['href'] = reverse('user:login')
            return JsonResponse(self.ret_msg)

        comment_data = self.clean_data(request)
        if comment_data:
            self.create_comment(data=comment_data)
            self.ret_msg['status'] = 1
        else:
            self.ret_msg['msg']['msg'] = "数据不完整"
        self.ret_msg['msg']= request.user.avatar.url

        return JsonResponse(self.ret_msg)


    @staticmethod
    def create_comment(data: dict):
        print(data)
        try:
            obj = Comment.objects.create(**data)
            obj.save()
        except Exception as e:
            print(e)

    @staticmethod
    def clean_data(request):
        content = request.POST.get("content")
        content = content if len(content) < 200 else content[:200]
        target_id = request.POST.get('target_id')
        owner = request.user

        if all((content, target_id, owner,)) and owner.username:

            return {
                'content': content,
                'target_id': target_id,
                'owner': owner,
                'nickname': request.user.nickname,
            }