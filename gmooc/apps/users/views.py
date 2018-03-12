import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic.base import View
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from organizations.models import Teacher, CourseOrg
from courses.models import Course
from operations.models import UserCourse, UserFavorite, UserMessage
from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, PwdResetForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


class CustomAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception:
            return None


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"msg": "该用户已存在", "register_form": register_form})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()
            send_register_email(user_name, "register")
            return render(request, "login.html", {})
        else:
            return render(request, "register.html", {"register_form": register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, "login.html", {})
        else:
            return render(request, "active_fail.html")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(request, username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html", {"username": user_name})
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！", "login_form": login_form})
        else:
            return render(request, "login.html", {"login_form": login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_status = send_register_email(email, "forget")
            if send_status:
                return render(request, "send_success.html")
            else:
                return render(request, "forgetpwd.html", {"msg": "邮件发送失败", "forget_form": forget_form})
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class PwdResetView(View):
    def get(self, request, code):
        all_records = EmailVerifyRecord.objects.filter(code=code)
        if all_records:
            for record in all_records:
                email = record.email
            return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")


class PwdModifyView(View):
    def post(self, request):
        reset_form = PwdResetForm(request.POST)
        if reset_form.is_valid():
            email = request.POST.get("email", "")
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 == pwd2:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pwd1)
                user.save()
                return render(request, "login.html")
            else:
                return render(request, "password_reset.html", {"msg": "两个密码不一致", "reset_form": reset_form, "email": email})
        else:
            return render(request, "password_reset.html", {"reset_form": reset_form})


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'info'
        return render(request, "usercenter-info.html", {"current_page": current_page})

    def post(self, request):
        userinfo_form = UserInfoForm(request.POST, instance=request.user)
        if userinfo_form.is_valid():
            userinfo_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(userinfo_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail"}', content_type='application/json')


class UserModifyPwdView(LoginRequiredMixin, View):
    def post(self, request):
        reset_form = PwdResetForm(request.POST)
        if reset_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 == pwd2:
                user = request.user
                user.password = make_password(pwd1)
                user.save()
                return HttpResponse('{"status": "success"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "密码不一致"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(reset_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get("email", "")
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "该邮箱已存在"}', content_type='application/json')
        else:
            send_status = send_register_email(email, "modify_email")
        if send_status:
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"email": "验证码发送失败"}', content_type='application/json')


class ModifyEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")
        if EmailVerifyRecord.objects.filter(email=email, code=code, send_type="modify_email"):
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status": "success"}', content_type="application/json")
        else:
            return HttpResponse('{"email": "验证码验证失败"}', content_type="application/json")


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'course'
        user_courses = UserCourse.objects.filter(user=request.user)
        all_mycourses = [user_course.course for user_course in user_courses]
        return render(request, "usercenter-mycourse.html", {
            "all_mycourses": all_mycourses,
            "current_page": current_page,
        })


class MyFavView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'fav'
        fav_teachers = []
        fav_orgs = []
        fav_courses = []
        fav_type = request.GET.get("type", "")
        if fav_type == "teacher":
            user_favs = UserFavorite.objects.filter(user=request.user, fav_type=3)
            fav_teacher_ids = [user_fav.fav_id for user_fav in user_favs]
            fav_teachers = Teacher.objects.filter(id__in=fav_teacher_ids)
        elif fav_type == "org":
            user_favs = UserFavorite.objects.filter(user=request.user, fav_type=2)
            fav_org_ids = [user_fav.fav_id for user_fav in user_favs]
            fav_orgs = CourseOrg.objects.filter(id__in=fav_org_ids)
        else:
            user_favs = UserFavorite.objects.filter(user=request.user, fav_type=1)
            fav_course_ids = [user_fav.fav_id for user_fav in user_favs]
            fav_courses = Course.objects.filter(id__in=fav_course_ids)
        return render(request, "usercenter-fav.html", {
            "current_page": current_page,
            "fav_type": fav_type,
            "fav_orgs": fav_orgs,
            "fav_courses": fav_courses,
            "fav_teachers": fav_teachers,
        })


class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_msg in unread_messages:
            unread_msg.has_read = True
            unread_msg.save()
        return render(request, "usercenter-message.html", {
            "all_messages": all_messages,
            "current_page": 'message',
        })


class IndexView(View):
    def get(self, request):
        all_banners = Banner.objects.all().order_by("index")[:5]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        courses = Course.objects.filter(is_banner=False)[:6]
        orgs = CourseOrg.objects.all()[:15]
        return render(request, "index.html", {
            "all_banners": all_banners,
            "banner_courses": banner_courses,
            "courses": courses,
            "orgs": orgs,
        })
