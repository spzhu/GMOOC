from django.urls import path

from .views import CourseListView, CourseDetailView, CourseLessonView, CourseCommentView, AddCommentView, VideoPlayView

app_name = "course"
urlpatterns = [
    path("list/", CourseListView.as_view(), name="course_list"),
    path("detail/<int:course_id>/", CourseDetailView.as_view(), name="course_detail"),
    path("lesson/<int:course_id>/", CourseLessonView.as_view(), name="course_lesson"),
    path("comment/<int:course_id>/", CourseCommentView.as_view(), name="course_comment"),
    path("add_comment/", AddCommentView.as_view(), name="add_comment"),
    path("video/<int:video_id>/", VideoPlayView.as_view(), name="video_play"),
]
