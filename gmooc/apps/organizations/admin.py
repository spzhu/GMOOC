from django.contrib import admin

from .models import City, CourseOrg, Teacher
# Register your models here.


class CityAdmin(admin.ModelAdmin):
    pass


class CourseOrgAdmin(admin.ModelAdmin):
    pass


class TeacherAdmin(admin.ModelAdmin):
    pass


admin.site.register(City, CityAdmin)
admin.site.register(CourseOrg, CourseOrgAdmin)
admin.site.register(Teacher, TeacherAdmin)
