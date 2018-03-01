from datetime import datetime

from django.db import models

# Create your models here.


class Course(models.Model):
    """
    课程基本信息表
    """
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=100, verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程难度")
    degree = models.CharField(max_length=10, choices=(("jc", "初级"), ("zj", "中级"), ("gj", "高级")), verbose_name="课程难度")
    learn_time = models.IntegerField(default=0, verbose_name="学习时长(分钟)")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="课程封面")
    click_nums = models.IntegerField(default=0, verbose_name="点击量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    课程章节信息
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):
    """
    视频信息
    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="章节")
    name = models.CharField(max_length=100, verbose_name="视频名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    """
    课程资源
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="课程资源名")
    download = models.FileField(upload_to="courses/resource/%Y/%m", verbose_name="资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
