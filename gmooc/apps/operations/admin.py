from django.contrib import admin

from .models import UserAsk, UserCourse, UserMessage, UserFavorite, CourseComments
# Register your models here.


class UserAskAdmin(admin.ModelAdmin):
    pass


class UserCourseAdmin(admin.ModelAdmin):
    pass


class UserMessageAdmin(admin.ModelAdmin):
    pass


class UserFavoriteAdmin(admin.ModelAdmin):
    pass


class CourseCommentsAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserAsk, UserAskAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(UserMessage, UserMessageAdmin)
admin.site.register(UserFavorite, UserFavoriteAdmin)
admin.site.register(CourseComments, CourseCommentsAdmin)
