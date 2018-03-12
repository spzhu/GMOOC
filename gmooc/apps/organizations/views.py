from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q

from pure_pagination import Paginator, PageNotAnInteger
from operations.models import UserFavorite
from courses.models import Course
from .models import City, CourseOrg, Teacher
from .forms import UserAskForm
# Create your views here.


class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get("fav_id", "")
        fav_type = request.POST.get("fav_type", "")
        if request.user.is_authenticated:
            exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
            if int(fav_type) == 1:
                fav_object = Course.objects.get(id=int(fav_id))
            elif int(fav_type) == 2:
                fav_object = CourseOrg.objects.get(id=int(fav_id))
            elif int(fav_type) == 3:
                fav_object = Teacher.objects.get(id=int(fav_id))
            if exist_record:
                exist_record.delete()
                fav_object.fav_nums -= 1
                fav_object.save()
                return HttpResponse('{"status": "success", "msg": "收藏"}', content_type='application/json')
            else:
                if int(fav_id) > 0 and int(fav_type) > 0:
                    user_fav = UserFavorite()
                    user_fav.user = request.user
                    user_fav.fav_id = int(fav_id)
                    user_fav.fav_type = int(fav_type)
                    user_fav.save()
                    fav_object.fav_nums += 1
                    fav_object.save()
                    return HttpResponse('{"status": "success", "msg": "已收藏"}', content_type='application/json')
                else:
                    return HttpResponse('{"status": "fail", "msg": "收藏失败"}', content_type='application/json')

        else:
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')


class OrgDetailView(View):
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=org_id)
        course_org.click_nums += 1
        course_org.save()
        # 利用外键取值，django ORM
        all_courses = course_org.course_set.all()
        all_teacher = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, "org-detail-homepage.html", {
            "all_courses": all_courses,
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=org_id)
        # 利用外键取值，django ORM
        all_courses = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, "org-detail-course.html", {
            "all_courses": all_courses,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=org_id)
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # 利用外键取值，django ORM
        return render(request, "org-detail-desc.html", {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=org_id)
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # 利用外键取值，django ORM
        all_teacher = course_org.teacher_set.all()
        return render(request, "org-detail-teacher.html", {
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgListView(View):
    def get(self, request):
        all_cities = City.objects.all()
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:5]
        keyword = request.GET.get("keywords", "")
        if keyword:
            all_orgs = all_orgs.filter(Q(name__icontains=keyword)|
                                       Q(desc__icontains=keyword))
        city_id = request.GET.get("city", "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get("sort", "")
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-courses")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)
        return render(request, "org-list.html", {
            "all_cities": all_cities,
            "all_orgs": orgs,
            "org_nums": all_orgs.count(),
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
        })


class UserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # modelform的save方法直接存入数据库
            userask_form.save(commit=True)
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        hot_teachers = all_teachers.order_by("-click_nums")[:3]
        keyword = request.GET.get("keywords", "")
        if keyword:
            all_teachers = all_teachers.filter(Q(name__icontains=keyword)|
                                               Q(work_company__icontains=keyword)|
                                               Q(work_position__icontains=keyword))
        sort = request.GET.get("sort")
        if sort == "hot":
            all_teachers = all_teachers.order_by("-click_nums")
        else:
            pass
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_teachers, 2, request=request)
        teachers = p.page(page)
        return render(request, "teacher-list.html", {
            "all_teachers": teachers,
            "teacher_nums": all_teachers.count(),
            "hot_teachers": hot_teachers,
            "sort": sort,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.click_nums += 1
        teacher_courses = teacher.course_set.all()
        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_fav_org = True
        else:
            pass
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(teacher_courses, 2, request=request)
        courses = p.page(page)
        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "teacher_courses": courses,
            "hot_teachers": hot_teachers,
            "has_fav_org": has_fav_org,
            "has_fav_teacher": has_fav_teacher,
        })
