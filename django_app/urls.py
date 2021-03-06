"""sichuan_yd_children URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django_app.settings import MEDIA_ROOT
from django.conf.urls.static import static
import xadmin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),  #extra_apps/DjangoUeditor
]
urlpatterns += static('/media/', document_root=MEDIA_ROOT)

from rest_framework.documentation import include_docs_urls

urlpatterns += [
    #drf文档，title自定义
    path('docs',include_docs_urls(title='api文档')),
    path('api-auth/',include('rest_framework.urls')),
]


from goods.views import GoodsListViewSet,CategoryViewSet
from rest_framework.routers import DefaultRouter

from rest_framework_jwt.views import obtain_jwt_token
others = [
    path('login/', obtain_jwt_token),# 后台登录接口，登录成功返回token。每次请求，请求头自带token？
]
router = DefaultRouter()

#配置goods的url
router.register(r'goods', GoodsListViewSet)
# 配置Category的url
router.register(r'categorys', CategoryViewSet, base_name="categorys")
from users.views import SmsCodeViewset,UserViewset

# 配置codes的url
router.register(r'code', SmsCodeViewset, base_name="code")
router.register(r'users', UserViewset, base_name="users")
others.extend(router.urls)

# 版本控制 http://127.0.0.1:8000/api/v1/
apiversion_urls = [
    path('v1/', include(others)),
]

urlpatterns += [
    #商品列表页
    url('^api/', include(apiversion_urls)),
]
