from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Schedules



class SchedulesView(TemplateView):
    template_name = 'schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_schedules'] = Schedules.objects.all()
        return context