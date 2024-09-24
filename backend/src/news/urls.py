from django.contrib import admin
from django.urls import path, include
from .views import IndexView, NewsView, NewsDetailView



urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('news/', NewsView.as_view(), name='news'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail'),
]