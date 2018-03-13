from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from organizations.models import CourseOrg, Teacher
# Create your models here.


class Course(models.Model):
    """
    课程基本信息表
    """
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="课程机构", null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="课程讲师", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="课程名")
    is_banner = models.BooleanField(default=False, verbose_name="是否轮播")
    desc = models.CharField(max_length=100, verbose_name="课程描述")
    detail = UEditorField(verbose_name="课程详情", width=600, height=300, toolbars="full", imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default="", upload_settings={"imageMaxSize": 1204000})
    category = models.CharField(max_length=100, verbose_name="课程类型", default="后端开发")
    tag = models.CharField(max_length=100, verbose_name="课程标签", default="python")
    degree = models.CharField(max_length=10, choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), verbose_name="课程难度")
    learn_time = models.IntegerField(default=0, verbose_name="学习时长(分钟)")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="课程封面")
    click_nums = models.IntegerField(default=0, verbose_name="点击量")
    need_know = models.CharField(default="", max_length=100, verbose_name="课程须知")
    will_learn = models.CharField(default="", max_length=100, verbose_name="老师告诉你")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_chapter_nums(self):
        return self.lesson_set.all().count()

    def get_course_lessons(self):
        return self.lesson_set.all()


class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        # proxy参数设置为True，不会再生成第二张表
        proxy = True


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

    def get_lesson_videos(self):
        return self.video_set.all()


class Video(models.Model):
    """
    视频信息
    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="章节")
    name = models.CharField(max_length=100, verbose_name="视频名")
    url = models.CharField(max_length=100, verbose_name="视频链接", default="")
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
