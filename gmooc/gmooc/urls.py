"""gmooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import xadmin

# from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from gmooc import settings
from users.views import IndexView, LoginView, LogoutView, RegisterView, ActiveUserView, ForgetPwdView, PwdResetView, PwdModifyView

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('captcha/', include('captcha.urls')),
    path('active/<active_code>/', ActiveUserView.as_view(), name="user_active"),
    path('forget/', ForgetPwdView.as_view(), name="forget_pwd"),
    path('reset/<code>', PwdResetView.as_view(), name="reset"),
    path('pwd_reset/', PwdModifyView.as_view(), name="reset_pwd"),

    # 课程机构url配置
    path('org/', include('organizations.urls', namespace='org')),
    path('course/', include('courses.urls', namespace='course')),
    path('users/', include('users.urls', namespace='users')),

    # media上传文件url处理
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
