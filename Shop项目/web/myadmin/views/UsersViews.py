from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from django.contrib.auth.hashers import make_password, check_password
from .. models import Users
from web.settings import BASE_DIR
import os

# Create your views here.
# 用户模型的管理

# 用户列表
def user_index(request):
    try:
        # 获取所有用户数据
        data = Users.objects.all()

        # 获取搜索条件
        types = request.GET.get('types',None)
        keywords = request.GET.get('keywords',None)
        # 判断是否搜索
        if types == 'all':
            from django.db.models import Q
            data = data.filter(Q(id__contains=keywords)|Q(nikename__contains=keywords)|Q(email__contains=keywords)|Q(phone__contains=keywords))
        elif types :
            search = {types+'__contains':keywords}
            data = data.filter(**search)

        # 导入分页类
        from django.core.paginator import Paginator
        # 实例化分页类(每页显示几条)
        p = Paginator(data, 5)
        # 获取当前的页码数(第几页)
        pageindex = request.GET.get('page',1)
        # 获取当前页的数据
        userlist = p.page(pageindex)
        # 获取所有的页码
        # pages = p.page_range
        # pages = p.num_pages
        # 分配数据
        context = {'userlist':userlist}
        # 加载模板
        return render(request,'myadmin/users/index.html',context)
    except Exception as e:
        print('分页',e)
    
# 用户添加表单
def user_add(request):
    return render(request,'myadmin/users/add.html')

# 用户执行添加
def user_insert(request):
    # 接收表单数据
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')

    # 处理密码 加密
    data['password'] = make_password(data['password'], None, 'pbkdf2_sha256')

    # 头像上传
    # 接收上传的文件
    myfile = request.FILES.get('pic',None)
    if not myfile:
        # 没有选择头像上传,
        return HttpResponse('<script>alert("没有选择头像上传");history.back(-1);</script>')

    # 处理头像的上传  1.jpg ==> [1,jpg]
    data['pic_url'] = uploads_pic(myfile)
    
    try:
        # 创建模型,添加数据
        ob = Users(**data)
        ob.save()
        # 跳转到列表页
        return HttpResponse('<script>alert("添加成功");location.href="/myadmin/user/index/";</script>')
    except:
        pass
    return HttpResponse('<script>alert("添加失败");history.back(-1);</script>')

# 头像上传的处理代码
def uploads_pic(myfile):
    try:
        import time
        # 时间+图片名
        filename = str(time.time())+"."+myfile.name.split('.').pop()
        # 图片上传的目录
        destination = open(BASE_DIR+"/static/uploads/"+filename,"wb+")
        for chunk in myfile.chunks():# 分块写入文件  
            destination.write(chunk)  
        destination.close()
        return '/static/uploads/'+filename
    except Exception as e:
        print('头像上传处理错误',e)
        return False

# 用户编辑
def user_edit(request):

    # 接受用户id
    uid = request.GET.get('uid')
    # 获取当前用户对象
    ob = Users.objects.get(id = uid)


    # 判断当前的请求方式
    if request.method == 'POST':
        # 判断密码是否更新
        if request.POST.get('password',None):
        # 更新密码
            ob.password = make_password(request.POST['password'], None, 'pbkdf2_sha256')
        
        # 判断头像是否更新
        try:
            myfile = request.FILES.get('pic',None)
            print(myfile)
            if myfile:
                # 如果有新头像上传，则先删除原头像图片
                if ob.pic_url:
                    os.remove(BASE_DIR+ob.pic_url)
                # 再上传新的头像
                ob.pic_url = uploads_pic(myfile)
        except Exception as e:
            print('头像更新操作',e)
        # 判断是否有传值
        if request.POST.get('age'):
            ob.age = request.POST.get('age')


        # 更新其它字段
        try:
            ob.nikename = request.POST.get('nikename',None)
            ob.email = request.POST.get('email',None)
            ob.phone = request.POST.get('phone',None)
            ob.sex = request.POST.get('sex',None)
            ob.save()
        except Exception as e:
            print('字段更新操作',e)
        return HttpResponse('<script>alert("更新成功");location.href="/myadmin/user/index/";</script>')

    else:
        # 显示编辑表单
        context = {'uinfo':ob}
        return render(request,'myadmin/users/edit.html',context)

# 用户状态跟新
def user_set_status(request):
    # 通过uid获取当前用户对象
    ob = Users.objects.get(id=request.GET.get('uid'))
    ob.status = request.GET.get('status')
    ob.save()
    return JsonResponse({'msg':'状态更新成功','code':0})