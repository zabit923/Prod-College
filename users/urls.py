from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import UserProfileView, login, logout, TeacherProfile, add_lecture, delete_lecture, LectureDetail, \
    SchedulesView, AllTeachers, PublicTeacherProfile


app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('teacher-profile/<int:teacher_id>/', TeacherProfile.as_view(), name='teacher_profile'),
    path('add_lecture/', add_lecture, name='add_lecture'),
    path('delete_lecture/<int:lecture_id>/', delete_lecture, name='delete_lecture'),
    path('lecture/<int:pk>/', LectureDetail.as_view(), name='lecture_detail'),
    path('schedules/', SchedulesView.as_view(), name='schedules'),
    path('all_teachers/', AllTeachers.as_view(), name='blog'),
    path('public_profile_teacher/<int:teacher_id>/', PublicTeacherProfile.as_view(), name='public_profile'),
    path('logout/', logout, name='logout'),
]