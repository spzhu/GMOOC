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
    click_nums = models.IntegerField(default=0, verbose_name="点击量")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏量")
    image = models.ImageField(upload_to="organizations/%Y/%m", verbose_name="机构封面")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="城市")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "机构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """
    教师信息
    """
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构")
    name = models.CharField(max_length=50, verbose_name="教师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=100, verbose_name="就职公司")
    work_positon = models.CharField(max_length=100, verbose_name="公司职位")
    feature = models.CharField(max_length=100, verbose_name="教学特点", default="")
    click_nums = models.IntegerField(default=0, verbose_name="点击量")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
