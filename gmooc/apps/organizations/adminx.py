import xadmin

from .models import City, CourseOrg, Teacher


class CityAdmin:
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin:
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city__name', 'add_time']
    # 当有外键的时候以ajax加载的方式显示数据，防止数据量过大，下拉菜单过长
    relfield_style = 'fk_ajax'


class TeacherAdmin:
    list_display = ['name', 'org', 'work_years', 'work_company', 'work_position', 'feature', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'feature']
    list_filter = ['org__name', 'name', 'work_years', 'work_company', 'work_position', 'feature', 'click_nums', 'fav_nums', 'add_time']


xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
