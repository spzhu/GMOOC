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
