import xadmin

from .models import City, CourseOrg, Teacher


class CityAdmin:
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin:
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'city']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'city__name', 'add_time']


class TeacherAdmin:
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_positon', 'feature', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_positon', 'feature']
    list_filter = ['org__name', 'name', 'work_years', 'work_company', 'work_positon', 'feature', 'click_nums', 'fav_nums', 'add_time']


xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
