from django.contrib import admin

from .models import Course, Lesson, Video, CourseResource, BannerCourse
# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    pass


class LessonAdmin(admin.ModelAdmin):
    pass


class VideoAdmin(admin.ModelAdmin):
    pass


class CourseResourceAdmin(admin.ModelAdmin):
    pass


class BannerCourseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(CourseResource, CourseResourceAdmin)
admin.site.register(BannerCourse, BannerCourseAdmin)
