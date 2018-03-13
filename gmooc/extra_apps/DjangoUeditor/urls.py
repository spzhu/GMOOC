#coding:utf-8
from django import VERSION
if VERSION[0:2]>(1,9):
    from django.urls import re_path
else:
    pass

from views import get_ueditor_controller

urlpatterns = [
    re_path(r'^controller/$', get_ueditor_controller),
]
