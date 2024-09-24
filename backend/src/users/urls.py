from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import (UserProfileView, login,
                    logout, TeacherProfile,
                    AllTeachers, PublicTeacherProfile,
                    add_personal_link, delete_personal_link,
                    delete_link)


app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('teacher-profile/<int:teacher_id>/', TeacherProfile.as_view(), name='teacher_profile'),
    path('add_personal_link/', add_personal_link, name='add_personal_link'),
    path('delete_personal_link/<int:link_id>/', delete_personal_link, name='delete_personal_link'),
    path('delete_link/<int:link_id>/', delete_link, name='delete_link'),
    path('all_teachers/', AllTeachers.as_view(), name='blog'),
    path('public_profile_teacher/<int:teacher_id>/', PublicTeacherProfile.as_view(), name='public_profile'),
    path('logout/', logout, name='logout'),
]
