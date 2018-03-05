from django.urls import path

from .views import OrgListView, UserAskView, OrgDetailView, OrgDescView, OrgCourseView, OrgTeacherView, AddFavView

app_name = "org"
urlpatterns = [
    path('list/', OrgListView.as_view(), name="org_list"),
    path('add_ask/', UserAskView.as_view(), name="add_ask"),
    path('org_home/<int:org_id>/', OrgDetailView.as_view(), name="org_home"),
    path('org_course/<int:org_id>/', OrgCourseView.as_view(), name="org_course"),
    path('org_desc/<int:org_id>/', OrgDescView.as_view(), name="org_desc"),
    path('org_teacher/<int:org_id>/', OrgTeacherView.as_view(), name="org_teacher"),
    path('add_fav/', AddFavView.as_view(), name="add_fav"),
]
