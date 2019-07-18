from django.shortcuts import render
from django.http import HttpResponse
import re

class AdminLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        # 用户的请求路径
        # 定义允许访问的路径
        arr = ['/myadmin/login/','/myadmin/dologin/','/myadmin/verifycode/']
        path = request.path
        # 检测用户是否访问后台
        if re.match('/myadmin/',path) and path not in arr:
            # 检测是否已经登录
            AdminUser = request.session.get('AdminUser',None)
            if not AdminUser:
                # 没有登录
                return HttpResponse('<script>alert("请先登录");location.href="/myadmin/login/"</script>')

        response = self.get_response(request)
        return response