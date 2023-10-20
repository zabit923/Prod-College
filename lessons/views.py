from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Schedules



class SchedulesView(TemplateView):
    template_name = 'schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_teacher:
            context['all_schedules'] = Schedules.objects.all()
        else:
            context['all_schedules'] = Schedules.objects.filter(course=user.course)
        return context
