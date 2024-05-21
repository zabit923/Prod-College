from django.urls import path

from .views import add_lecture, add_review, delete_lecture, delete_review, LectureDetail, SchedulesView


app_name = 'data'

urlpatterns = [
    path('add_lecture/', add_lecture, name='add_lecture'),
    path('add_review/<int:pk>/', add_review, name='add_review'),
    path('delete_lecture/<int:lecture_id>/', delete_lecture, name='delete_lecture'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),
    path('lecture/<int:pk>/', LectureDetail.as_view(), name='lecture_detail'),
    path('schedules/', SchedulesView.as_view(), name='schedules'),
]
