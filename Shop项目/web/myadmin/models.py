from django.db import models

# Create your models here.


# 定义用户模型
class Users(models.Model):
    nikename = models.CharField(max_length=20,null=True)
    password = models.CharField(max_length=77)
    # phone = models.CharField(max_length=11,unique=True)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    pic_url = models.CharField(max_length=100)
    SEX_CHOICES = (
        (0, '女'),
        (1, '男'),
    )
    sex = models.CharField(max_length=1,null=True,choices=SEX_CHOICES)
    # 0 正常  1禁用 
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)


# 商品分类模型
class Cates(models.Model):
    name = models.CharField(max_length=20)
    pid = models.IntegerField()
    path = models.CharField(max_length=50)

# 商品模型
class Goods(models.Model):
    # id 所属分类，商品名，图片，添加时间，销量

    cateid = models.ForeignKey(to="Cates",to_field="id")
    goodsname = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    price = models.FloatField()
    goodsnum = models.IntegerField()
    pic_url = models.CharField(max_length=255)
    goodsinfo = models.TextField()
    ordernum = models.IntegerField(default=0)
    clicknum = models.IntegerField(default=0)
    # 0新品，1热卖，2，推荐，下架
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)
