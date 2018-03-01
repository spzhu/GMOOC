import xadmin

from xadmin import views
from .models import EmailVerifyRecord, Banner


class BaseSetting:
    # 启用主题选择
    enable_themes = True
    use_bootswatch = True


class GlobalSetting:
    # 修改title
    site_title = "慕学后台管理系统"
    # 修改footer
    site_footer = "慕学在线网"
    # 设置菜单栏收起选项
    menu_style = "accordion"


class EmailVerifyRecordAdmin:
    # list_display变量在后台列表显示要展示的字段
    list_display = ['code', 'email', 'send_type', 'send_time']
    # search_fields搜索功能
    search_fields = ['code', 'email', 'send_type']
    # 筛选字段
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin:
    list_display = ['title', 'url', 'index', 'add_time']
    search_fields = ['title', 'url', 'index']
    list_filter = ['title', 'url', 'index', 'add_time']

# xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
# 注册setting
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
