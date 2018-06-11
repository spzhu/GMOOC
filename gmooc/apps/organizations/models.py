from datetime import datetime

from django.db import models

# Create your models here.


class City(models.Model):
    """
    城市信息
    """
    name = models.CharField(max_length=100, verbose_name="城市名")
    desc = models.TextField(verbose_name="城市描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    """
    课程机构
    """
    name = models.CharField(max_length=100, verbose_name="机构名称")
    desc = models.TextField(verbose_name="机构描述")
    tag = models.CharField(max_length=10, verbose_name="机构标签", default="知名高校")
    category = models.CharField(max_length=20, choices=(("pxjg", "培训机构"), ("gr", "个人"), ("gx", "高校")), verbose_name="机构类别", default="pxjg")
    click_nums = models.IntegerField(default=0, verbose_name="点击量")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏量")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    courses = models.IntegerField(default=0, verbose_name="课程数")
    image = models.ImageField(upload_to="organizations/%Y/%m", verbose_name="logo", null=True, blank=True)
    address = models.CharField(max_length=150, verbose_name="机构地址")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="城市")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_nums(self):
        return self.course_set.all().count()

    def get_teacher_nums(self):
        return self.teacher_set.all().count()


class Teacher(models.Model):
    """
    教师信息
    """
    name = models.CharField(max_length=50, verbose_name="教师名")
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构")
    image = models.ImageField(upload_to="teachers/%Y/%m", verbose_name="头像")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=100, verbose_name="就职公司")
    work_position = models.CharField(max_length=100, verbose_name="公司职位")
    feature = models.CharField(max_length=100, verbose_name="教学特点", default="")
    click_nums = models.IntegerField(default=0, verbose_name="点击量")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_nums(self):
        return self.course_set.all().count()
