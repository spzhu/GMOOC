import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse


class LessonInline:
    model = Lesson
    extra = 0


class CourseResourceInline:
    model = CourseResource
    extra = 0


class CourseAdmin:
    list_display = ['name', 'desc', 'degree', 'learn_time', 'students', 'fav_nums', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'degree', 'learn_time', 'students']
    list_filter = ['name', 'desc', 'degree', 'learn_time', 'students', 'add_time']
    ordering = ['-click_nums']
    readonly_fields = ['click_nums']
    exclude = ['fav_nums']
    inlines = [LessonInline, CourseResourceInline]
    list_editable = ['degree']
    style_fields = {'detail': 'ueditor'}
    import_excel = True

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    # 统计当前信息
    def save_models(self):
        obj = self.new_obj  # 取到当前实例
        obj.save()
        if obj.course_org:
            course_org = obj.course_org
            course_org.courses = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super().post(request, *args, **kwargs)


class BannerCourseAdmin:
    list_display = ['name', 'desc', 'degree', 'learn_time', 'students', 'fav_nums', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'degree', 'learn_time', 'students']
    list_filter = ['name', 'desc', 'degree', 'learn_time', 'students', 'add_time']
    ordering = ['-click_nums']
    readonly_fields = ['click_nums']
    exclude = ['fav_nums']
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


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
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
