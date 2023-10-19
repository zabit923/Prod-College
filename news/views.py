from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from django.http import JsonResponse
from .models import News




class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.order_by('-created_at')[:3]
        return context


class NewsView(TemplateView):
    template_name = 'news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_news'] = News.objects.order_by('-created_at')
        return context


class NewsDetailView(DetailView):
    model = News
    slug_field = "slug"
    template_name = 'one-news.html'