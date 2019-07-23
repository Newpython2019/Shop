############### 其他模块 ###############
from django.shortcuts import render
from django.http import HttpResponse,Http404

# 精选品牌
def shop_SelectedBrands(request):
	return render(request,'myhome/order/SelectedBrands.html')
	

# 全球购
def shop_GlobalPurchase(request):
	return render(request,'myhome/order/GlobalPurchase.html')

# 品牌馆
def shop_BrandPavilion(request):
	return render(request,'myhome/order/BrandPavilion.html')
	