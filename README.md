# similal_taobao
类似淘宝的一个后端数据支持网站

###项目创建逻辑
1. 先创建基本配置，可以拷贝[默认django配置](https://github.com/yangtao4389/default_django2.0)
2. 创建apps，将apps里面的用户，商品等加入后把model写好。注意这里的users，因为继承了django中默认的用户表结构，所以需要将settings.py中也要写入AUTH_USER_MODEL = 'users.UserProfile' 。否则会报错
3. 可以直接运行，生成相关表了
4. extra_apps中，拷贝xadmin以及DjangoUeditor源码，xadmin做了相应配置。并且xadmin的表依赖于django中的user。
5. 生成xadmin相关的表，并且在apps里面所有模块配置好adminx文件。创建superuser用户，可以去后台查看相应数据了。
6. 为了导入测试数据，创建db_tools，类似django-model的方式来创建数据。直接执行相应文件即可。
7. 准备对外提供相应接口。采用drf框架
8. 全局url中先集成drf-docs文档与api-auth 权限认证 。建议将rest_framework源码加入到extra_apps里面，这样不用pip安装，并且还可以自己修改源码
    INSTALLED_APPS = [
    'rest_framework',
]
from rest_framework.documentation import include_docs_urls
urlpatterns = [
    #drf文档，title自定义
    path('docs',include_docs_urls(title='api文档')),
    path('api-auth/',include('rest_framework.urls')),
]
9. 创建第一个api视图  应用GoodsListViewSet，参考drf框架的ViewSet集合。然后注册到url中，此时，/docs可以用了。并且注意用api版本控制
from goods.views import GoodsListViewSet
from rest_framework.routers import DefaultRouter
#
router = DefaultRouter()

#配置goods的url
router.register(r'goods', GoodsListViewSet)

# 版本控制 http://127.0.0.1:8000/api/v1/
apiversion_urls = [
    path('v1/', include(router.urls)),
]

urlpatterns += [
    #商品列表页
    url('^api/', include(apiversion_urls)),
]

10. drf细化处理
+ 过滤器，参考：goods/filter.py  首先需要将 'django_filters',注册到apps中，然后将写好的过滤器类注入到views视图中的ViewSet
    # 设置filter的类为我们自定义的类
    from django_filters.rest_framework import DjangoFilterBackend
    filter_backends = (DjangoFilterBackend,)
    filter_class = GoodsFilter
 
+ 搜索  直接在ViewSet中注册
filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
search_fields = ('=name', 'goods_brief')
ordering_fields = ('sold_num', 'shop_price')

11. 解决跨域问题。
当前面api接口写好，能有数据时，前端浏览器报错-跨域问题  
[解决方法](https://stackoverflow.com/questions/22476273/no-access-control-allow-origin-header-is-present-on-the-requested-resource-i)






#### 架构设计
extra_apps   （扩展的源码包）  
apps              （放所有app）   
db_tools   （数据库相关）   **直接运行里面的py文件，就可以实现对数据库的导入问题。这种方式一定要借鉴！！！**    
把extra_apps和apps标记为sources root,然后settings中也要加路径  

#### apps
users  用户  #model中 settings.py中重写了 AUTH_USER_MODEL = 'users.UserProfile' 该Model UserProfile  必须要继承from django.contrib.auth.models import AbstractUser
goods  商品  #model中的分类用了三级联动结构，用了关联自己的一个字段--parent_category
trade 交易  
user_operation  用户操作  
#### extra_apps 
xadmin  
    修改：plugins/ueditor 来配置DjangoUeditor 并注入到plugins/__init__的PLUGINS中
    配置url
        
DjangoUeditor  富文本  

#### 先跟着教程敲一遍
[Cnblog](http://www.cnblogs.com/derek1184405959/p/8733194.html)<br /> 

#### 注意
1. settings.py中重写了 AUTH_USER_MODEL = 'users.UserProfile' 该Model UserProfile  必须要继承from django.contrib.auth.models import AbstractUser
并且继承好后，必须生成migrations文档，这样xadmin中的migrations第一个文档才能继承AbstractUser 

2.xadmin中有几个依赖DjangoUeditor的地方，参考xadmin


