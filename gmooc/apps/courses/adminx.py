import xadmin

from .models import Course, Lesson, Video, CourseResource


class CourseAdmin:
    list_display = ['name', 'desc', 'degree', 'learn_time', 'students', 'fav_nums', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'degree', 'learn_time', 'students']
    list_filter = ['name', 'desc', 'degree', 'learn_time', 'students', 'add_time']


class LessonAdmin:
    list_display = ['name', 'course', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin:
    list_display = ['name', 'lesson', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin:
    list_display = ['name', 'course', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
