from extra_apps.rest_framework import mixins
from extra_apps.rest_framework import viewsets
from extra_apps.rest_framework.pagination import PageNumberPagination
from .models import Goods,GoodsCategory
from .serializers import GoodsSerializer,CategorySerializer
from .filters import GoodsFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
class GoodsPagination(PageNumberPagination):
    '''
    商品列表自定义分页
    '''
    #默认每页显示的个数
    page_size = 12
    #可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    #页码参数
    page_query_param = 'page'
    #最多能显示多少页
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    '商品列表页'

    # 认证试一下
    # from rest_framework.authentication import SessionAuthentication, BasicAuthentication
    # from rest_framework.permissions import IsAuthenticated
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)

    # def initialize_request(self, request, *args, **kwargs):
        # super().initialize_request(request, *args, **kwargs)
        # super(GoodsListViewSet, self).initialize_request(request, *args, **kwargs)
        # print(request.user)  #AnonymousUser


    # 分页
    pagination_class = GoodsPagination
    #这里必须要定义一个默认的排序,否则会报错
    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializer

    # 设置filter的类为我们自定义的类
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter

    # 搜索,=name表示精确搜索，也可以使用各种正则表达式
    # search_fields = ('=name', 'goods_brief')

    # # 搜索
    search_fields = ('name', 'goods_brief', 'goods_desc')
    # 排序
    ordering_fields = ('sold_num', 'shop_price')

class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品分类列表数据
    '''

    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer