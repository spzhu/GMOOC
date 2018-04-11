# GMOOC 实战学习笔记

### APP 设计

- courses 课程管理
- organization 机构和教师管理
- users 用户管理
- operation 操作管理

### models 设计

#### user model

-   继承django后台内置auth_user的model类AbstractUser

    ```
    from django.contrib.auth.models import AbstractUser


    class UserProfile(AbstractUser):
    ...

    ```
    自定义UserProfile覆盖默认的user表
-   EmailVerifyRecord 邮箱验证码
-   PageBanner 轮播图

#### course model
-   Course 课程基本信息表
    - 课程名字name
    - 课程描述desc
    - 课程详情detail
    - 课程难度degree
    - 学习时长learn_time
    - 学习人数students
    - 收藏人数fav_nums
    - 课程封面图片image
    - 点击量click_nums
    - 添加时间add_time
-   Lesson 课程章节，与Course为一对多的关系
    - 外键course，指向Course
    - 章节名name
    - 添加时间add_time
-   Video 课程视频, 与Lession对应
    - 外键lesson, 指向Lesson
    - 视频名name
    - 添加时间add_time
-   CourseResource课程资源, 与Course对应
    - 外键course, 指向Course
    - 资源名name
    - 添加时间add_time
    - 文件地址download(FileField)

#### organization model
-   CourseOrg 课程机构信息
    - 机构名称name
    - 机构描述desc
    - 点击数click_nums
    - 收藏数fav_nums
    - 封面image
    - 所在城市city，外键City
    - 添加时间add_time
-   Teacher 教师信息
    - 教师名name
    - 教学年限work_years
    - 就职公司work_company
    - 公司职位work_position
    - 教学特点feature
    - 所属机构org,外键CoursrOrg
    - 点击数click_nums
    - 收藏数fav_nums
    - 添加时间add_time
-   City 城市信息
    - 城市名name
    - 描述desc
    - 添加时间add_time

#### 上层operation model
-   UserAsk 用户咨询
-   CourseComments 用户评论
-   UserFavorite 用户收藏
-   UserMessage 用户消息
-   UserCourse 用户学习的课程

### django-admin后台管理系统

注册自定义的UserProfile，在users/admin.py文件中加入

```

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)
```

### Xadmin使用
- model注册与admin基本相同
- 页面显示的models名称为配置的Meta信息
- django后台是对表的增删改查，不依赖于业务逻辑

**xadmin参数**
- list_display,数组类型，设置后台界面要显示的model字段
- search_fields,数组，在后台界面增加搜索框，检索
- list_filter,数组，过滤器

**xadmin注册model处理外键的方式**
> list_filter中使用类似course__name的方式，使用"__"连接外键与外表字段名

#### xadmin全局配置
**主题设置, title,footer设置**
```
from xadmin import views

class BaseSetting:
    enable_themes = True
    use_boostwatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)
```

**修改app中文名**
在app如Courses文件夹下自动生成的apps.py文件中配置app
```
class CoursesConfig(AppConfig):
    name = "courses"
    verbose_name = "课程管理"
```
修改__init__.py文件，增加
```
default_app_config = "courses.apps.CoursesConfig"
```
### 用户注册页面

修改register.html的css等静态文件

**django template语法**
> 使用static前需要load
```
{% load static %}
href="{% static 'css/reset.css' %}"
```
django会根据settings中的STATIC_URL设置自动修改静态文件路径

**验证码插件**
> django-simple-captcha

### 机构列表页面

#### 处理ImageField的图片加载
1. html文档 img标签的data-url="{{ MEDIA_URL }}{ org.image }"
2. urls.py配置处理media资源的url，要用到django内建函数serve,
代码参考django文档
```
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

# ... the rest of your URLconf goes here ...

if settings.DEBUG:
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
            }),
]
```
3. settings配置
TEMPLATES 的 OPTIONS 添加'django.template.context_processors.media'，使得html中{{ MEDIA_URL }}可用

#### 分页功能

> 第三方库django-pure-pagination

具体使用方法见[github文档](https://github.com/jamespacileo/django-pure-pagination/blob/master/README.rst)

#### 筛选功能

model中的外键在数据库中是以_id后缀形式存储字段的，如外键city在数据表中字段为city_id,可以直接使用city_id做filter

#### ModelForm

可以指定相应Model的某些字段生成Form，并且可以对字段进行合法性判断
```
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = [...]
```
UserAskModel继承django的ModelForm,ModelForm可以定义Meta类，model参数指定Model类，fields参数指定转换为form的字段。

**验证字段是否合法**

定义clean_开头的方法，clean_+字段名，使用内置的cleaned_data提取字段值，进行验证。
```
def clean_mobile(self):
    mobile = self.cleaned_data['mobile']
    reg_mobile = '^1[3|4|5|7|8][0-9]{9}$'
    reg = re.compile(reg_mobile)
    if reg.match(mobile):
        return mobile
    else:
        raise forms.ValidationError("手机号码非法", code="invalid mobile")
```

### 课程页面

**学习过该课程的用户还学过哪些课**

通过UserCourse获取到学习该课程的user_ids列表，使用user_id__in=user_ids传入id列表，查询所有在id列表的UserCourse
同样的方法查询到全部关联课程

通过view实现登录权限的认证, 自定义LoginView

```
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin:

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
```

需要权限认证的View继承LoginRequiredMixin，View

```
class CourseLessonView(LoginRequiredMixin, View):
    ...
```

### 首页

#### 搜索功能

name__icontains=keyword, __icontains表示django model会转化为LIKE的SQL语句
django.db.models class Q 在检索或(|)、与(&)用于连接条件

### 个人页面

- 修改头像，使用新的View post方法
- 上传的文件位于request.FILES

### 404和500页面

在urls.py配置handler404、handler500
定义404和500的处理方法

```
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.internal_error'
```

```
def page_not_found(request):
    response = render_to_response('404.html')
    response.status_code = 404
    return response
```
> 注：hanler404与handler500的默认处理函数的template_name='404.html'和'500.html',只需将配置好的html文件改名为404.html和500.html,放在templates文件夹即可调用

DEBUG由True修改为False之后，django服务器不会再做静态文件的代理，不会再从配置的STATIC地址寻找静态文件
可以在settings自己指定STATIC_ROOT
```
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

### 网络安全

#### sql注入攻击

在用户输入的内容插入特殊字符，构造SQL语句进行sql注入攻击

#### xss攻击

> 跨站脚本攻击(Cross Site Scripting)

在用户访问的url中插入js脚本，执行脚本获取用户Cookie等信息

**防护**

- 对用户的输入进行长度和特殊字符的过滤
- 避免直接在cookie中泄露用户隐私
- 通过使cookie和ip绑定的方式来降低cookie泄露后的危险
- 尽量采用POST而非GET提交表单

#### csrf攻击
> 跨站请求伪造(Cross-site request forgery)

用户在访问服务器A的同时，访问了危险服务器B，B返回的html中带有一个指向A的url，比如一张图片的src设置了指向A的url请求，
使得用户浏览器携带访问A的seeionid去访问A，这样就进行了跨站请求伪造

### Xadmin进阶开发

#### 常用功能

- 修改默认排序 ordering=[]
- 设置只读字段 readonly_fields=[]
- 设置不显示的字段 exclude=[]
- 在显示列表增加修改功能list_editable=[]
- 设置每隔多长时间(秒)刷新refresh_times = [3, 5]
- 一个界面增加两种model数据，外键适用inlines=[LessonInline]

```
class LessonInline:
    model = Lesson
    extra = 0
```

过滤数据

```
def queryset(self):
    qs = super(CourseAdmin, self).queryset()
    qs = qs.filter(is_banner=False)
    return qs
```

统计保存model信息

```
def save_models(self):
    obj = self.new_obj  # 取到当前实例
    obj.save()
    if obj.course_org:
    course_org = obj.course_org
    course_org.courses = Course.objects.filter(course_org=course_org).count()
    course_org.save()
```

#### 富文本集成

> 插件DjangoUeditor

1.  安装DjangoUeditor for Django2[github](https://github.com/zhangfisher/DjangoUeditor)
2.  在settings配置INSTALLED_APPS
    ```
    INSTALLED_APPS = [
        'DjangoUeditor'
    ]
    ```
3.  在model中导入UEditorField
    ```
    from DjangoUeditor.models import UEditorField
    ...


    detail = UEditorField(verbose_name="课程详情", width=600, height=300, toolbars="full", imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default="", upload_settings={"imageMaxSize": 1204000})
    ```
4.  在xadmin的plugins文件增加ueditor文件,在xadmin的plugins包的__init__.py文件的PLUGINS参数增加ueditor插件
    ```
    PLUGINS = (
        ...
        'ueditor'
    )
    ```
5.  在adminx.py注册的Admin类添加字段style设置style_fields
    ```
    class CourseAdmin:
        ...
        style_fields = {'detail': 'ueditor'}
    ```
6.  template文件显示富文本的地方关闭自动转义
    ```
    {% autoescape off %}
    ...
    {% endautoescape %}
    ```

#### Nginx配置
```
# the upstream component nginx needs to connect to
upstream django {
# server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server 127.0.0.1:8000; # for a web port socket (we'll use this first)
}
# configuration of the server

server {
# the port your site will be served on
    listen      80;
# the domain name it will serve for
    server_name 127.0.0.1 ; # substitute your machine's IP address or FQDN
        charset     utf-8;

# max upload size
    client_max_body_size 75M;   # adjust to taste

# Django media
    location /media  {
        alias /home/spzhu/py_projects/GMOOC/gmooc/media;  # 指向django的media目录
    }

    location /static {
        alias /home/spzhu/py_projects/GMOOC/gmooc/static; # 指向django的static目录
    }

# Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     uwsgi_params; # the uwsgi_params file you installed
    }
}
```
