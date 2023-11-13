from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import UserProfileView, login, logout, TeacherProfile, add_lecture, delete_lecture, LectureDetail, \
    SchedulesView, AllTeachers, PublicTeacherProfile, add_personal_link, delete_personal_link, delete_link, \
    add_review, delete_review

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('teacher-profile/<int:teacher_id>/', TeacherProfile.as_view(), name='teacher_profile'),
    path('add_lecture/', add_lecture, name='add_lecture'),
    path('add_personal_link/', add_personal_link, name='add_personal_link'),
    path('add_review/<int:pk>/', add_review, name='add_review'),
    path('delete_lecture/<int:lecture_id>/', delete_lecture, name='delete_lecture'),
    path('delete_personal_link/<int:link_id>/', delete_personal_link, name='delete_personal_link'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),
    path('delete_link/<int:link_id>/', delete_link, name='delete_link'),
    path('lecture/<int:pk>/', LectureDetail.as_view(), name='lecture_detail'),
    path('schedules/', SchedulesView.as_view(), name='schedules'),
    path('all_teachers/', AllTeachers.as_view(), name='blog'),
    path('public_profile_teacher/<int:teacher_id>/', PublicTeacherProfile.as_view(), name='public_profile'),
    path('logout/', logout, name='logout'),
]