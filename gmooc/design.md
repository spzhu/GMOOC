# GMOOC 实战设计文档

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

### problems

#### makemigrations后migrate报错django.db.migrations.exceptions.InconsistentMigrationHistory
```
django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency users.0001_initial on database 'default'.
```
执行语句与已有数据库产生冲突，删除数据库表重新migrate

#### model 中出现的循环引用

> A import B ; B import A 产生死循环

**解决方法： APP models分层**

采用分层的app设计方式，使用更高层次的operation app操作model

#### models.ForeginKey报错
> TypeError: __init__() missing 1 required positional argument: 'on_delete'

django1.11以上ForeignKey有两个必需的参数to，on_delete  [django2.0_ForeignKey](https://docs.djangoproject.com/en/2.0/ref/models/fields/#foreignkey)
```
class ForeignKey(to, on_delete, **options)
```
