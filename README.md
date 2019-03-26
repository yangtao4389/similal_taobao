# similal_taobao
类似淘宝的一个后端数据支持网站


#### 架构设计
extra_apps   （扩展的源码包）  
apps              （放所有app）   
db_tools   （数据库相关）   **直接运行里面的py文件，就可以实现对数据库的导入问题。这种方式一定要借鉴！！！**    
把extra_apps和apps标记为sources root,然后settings中也要加路径  

#### apps
users  用户  #model中 settings.py中重写了 AUTH_USER_MODEL = 'users.UserProfile' 该Model UserProfile  必须要继承from django.contrib.auth.models import AbstractUser
goods  商品   
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


