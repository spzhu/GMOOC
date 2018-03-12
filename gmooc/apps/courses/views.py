from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger

from .models import Course, CourseResource, Video
from operations.models import UserCourse, UserFavorite, CourseComments
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all()
        hot_courses = all_courses.order_by("-click_nums")[:5]
        sort = request.GET.get("sort", "")
        keyword = request.GET.get("keywords", "")
        if keyword:
            all_courses = all_courses.filter(Q(name__icontains=keyword)|
                                             Q(desc__icontains=keyword)|
                                             Q(detail__icontains=keyword))
        if sort == "students":
            all_courses = all_courses.order_by("-students")
        elif sort == "hot":
            all_courses = all_courses.order_by("-click_nums")
        else:
            all_courses = all_courses.order_by("-add_time")
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)
        return render(request, "course-list.html", {
            "all_courses": courses,
            "hot_courses": hot_courses,
            "sort": sort,
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        course.save()
        user_course = UserCourse.objects.filter(course=course)
        related_courses = Course.objects.filter(tag=course.tag)[:3]
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        return render(request, "course-detail.html", {
            "course": course,
            "user_courses": user_course,
            "related_courses": related_courses,
            "has_fav_org": has_fav_org,
            "has_fav_course": has_fav_course,
        })


class CourseLessonView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.students += 1
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")
        all_lessons = course.get_course_lessons()
        all_resources = CourseResource.objects.filter(course=course)
        if not UserCourse.objects.filter(course=course, user=request.user):
            user_course = UserCourse()
            user_course.user = request.user
            user_course.course = course
            user_course.save()
        return render(request, "course-video.html", {
            "course": course,
            "all_lessons": all_lessons,
            "all_resources": all_resources,
            "related_courses": related_courses,
        })


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course_comments = CourseComments.objects.filter(course=course).order_by("-add_time")
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-comment.html", {
            "course": course,
            "course_comments": course_comments,
            "all_resources": all_resources,
        })


class AddCommentView(View):
    def post(self, request):
        if request.user.is_authenticated:
            course_id = request.POST.get("course_id", 0)
            comments = request.POST.get("comments", "")
            if int(course_id) > 0 and comments:
                course_comment = CourseComments()
                course_comment.user = request.user
                course_comment.course = Course.objects.get(id=int(course_id))
                course_comment.comments = comments
                course_comment.save()
                return HttpResponse('{"status": "success", "msg": "评论成功"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "评论失败"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')


class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=video_id)
        course = video.lesson.course
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")
        all_lessons = course.get_course_lessons()
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-play.html", {
            "course": course,
            "all_lessons": all_lessons,
            "all_resources": all_resources,
            "related_courses": related_courses,
            "video": video,
        })
