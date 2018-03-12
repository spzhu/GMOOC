from django.urls import path

from .views import UserInfoView, UploadImageView, UserModifyPwdView, SendEmailCodeView, ModifyEmailView
from .views import MyCourseView, MyFavView, MyMessageView


app_name = 'users'
urlpatterns = [
    path('info/', UserInfoView.as_view(), name="users_info"),
    path('upload_image/', UploadImageView.as_view(), name="upload_image"),
    path('modify_pwd/', UserModifyPwdView.as_view(), name="modify_pwd"),
    path('send_email_code/', SendEmailCodeView.as_view(), name="send_email_code"),
    path('modify_email/', ModifyEmailView.as_view(), name="modify_email"),
    path('mycourse/', MyCourseView.as_view(), name="mycourse"),
    path('my_fav/', MyFavView.as_view(), name="my_fav"),
    path('message/', MyMessageView.as_view(), name="message")
]
