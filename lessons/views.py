from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, TemplateView

from .forms import ReviewForm, LectureForm
from .models import Lecture, Reviews, Schedules


def add_review(request, pk):
    lecture = get_object_or_404(Lecture, id=pk)

    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.user
            text = form.cleaned_data['text']
            file = form.cleaned_data['file']
            review = Reviews(name=name, text=text, file=file, lecture=lecture)
            review.save()

    if request.user.is_teacher:
        teacher_profile_url = reverse('users:teacher_profile', args=(lecture.lecturer.id,))
        return redirect(teacher_profile_url)
    teacher_profile_url = reverse('users:public_profile', args=(lecture.lecturer.id,))
    return redirect(teacher_profile_url)


def delete_review(request, review_id):
    review = get_object_or_404(Reviews, pk=review_id)
    if request.user.is_teacher:
        review.delete()
    elif review.name == request.user:
        review.delete()

    if request.user.is_teacher:
        teacher_profile_url = reverse('users:teacher_profile', args=(review.lecture.lecturer.id,))
        return redirect(teacher_profile_url)
    teacher_profile_url = reverse('users:public_profile', args=(review.lecture.lecturer.id,))
    return redirect(teacher_profile_url)


def add_lecture(request):
    if request.method == 'POST':
        form = LectureForm(request.POST)
        if form.is_valid():
            lecturer = request.user
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            facult = form.cleaned_data['facult']
            course = form.cleaned_data['course']
            group = form.cleaned_data['group']
            lecture = Lecture(lecturer=lecturer, title=title, description=description, facult=facult, course=course,
                              group=group)
            lecture.save()

            teacher_id = request.user.pk
            profile_url = reverse('users:teacher_profile', args=(teacher_id,))
            return redirect(profile_url)
    else:
        form = LectureForm()

    return render(request, 'new_lesson.html', {'form': form})


def delete_lecture(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    if lecture.lecturer == request.user:
        lecture.delete()
        messages.success(request, 'Лекция успешно удалена.')
    else:
        messages.error(request, 'Вы не можете удалить эту лекцию.')

    teacher_id = request.user.pk
    profile_url = reverse('users:teacher_profile', args=(teacher_id,))
    return redirect(profile_url)


class LectureDetail(DetailView):
    model = Lecture
    template_name = 'lecture.html'
    context_object_name = 'lecture'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        facult = self.object.facult
        course = self.object.course
        group = self.object.group

        context['facult'] = facult
        context['course'] = course
        context['group'] = group

        return context


class SchedulesView(TemplateView):
    template_name = 'schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.is_teacher:
                context['all_schedules'] = Schedules.objects.all()
            else:
                context['all_schedules'] = Schedules.objects.filter(facult=user.facult)
        return context
