from django.http import JsonResponse
from django.views.generic import View
from ..config.models import Favorite
from libs.login_tools import required_login
# Create your views here.


class FavoriteView(View):
    """  """

    def __init__(self):
        self.ret = {"status": None, "msg": None}
        super().__init__()

    @required_login
    def post(self, request, *args, **kwargs):
        """ 收藏 """
        owner = request.user
        href = request.POST.get('href', None)
        title = request.POST.get('title', None)

        try:
            Favorite.objects.get_or_create(owner=owner, href=href, title=title)
            self.ret['status'] = True
        except Exception as e:
            # TODO log
            self.ret['msg'] = '500:服务端错误'
        return JsonResponse(self.ret)

