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

