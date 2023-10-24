from django.contrib import auth, messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from .forms import UserLoginForm, UserProfileForm, LectureForm, LinkForm
from .models import User, Course, TeacherLink
from lessons.models import Lecture, Schedules, RPD
from django.shortcuts import get_object_or_404




def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        student_id = request.POST['student_id']
        user = auth.authenticate(first_name=first_name, last_name=last_name, student_id=student_id)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('users:profile', args=[request.user.pk]))
        else:
            messages.error(request, 'Извините, нам пока не дали таблицу базы данных со всеми студентами, попробуйте '
                                    'войти в аккаунт попозже')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_teacher:
            context['form'] = UserProfileForm(instance=user, initial={'facult': user.facult, 'course': user.course})
        else:
            context['links'] = TeacherLink.objects.filter(faculty=user.facult, course=user.course)
        context['all_rpd'] = RPD.objects.filter(course=user.course, facult=user.facult)
        return context

    def post(self, request, *args, **kwargs):
        link_form = LinkForm(request.POST)
        if link_form.is_valid():
            facult = link_form.cleaned_data['facult']
            course = link_form.cleaned_data['course']
            link = link_form.cleaned_data['link']
            user = request.user
            existing_link = TeacherLink.objects.filter(teacher=user, faculty=facult, course=course).first()
            if existing_link:
                existing_link.link = link
                existing_link.save()
            else:
                new_link = TeacherLink(teacher=user, faculty=facult, course=course, link=link)
                new_link.save()

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class TeacherProfile(TemplateView):
    template_name = 'teacher-profile.html'

    def get(self, request, teacher_id):
        teacher = User.objects.get(id=teacher_id, is_teacher=True)
        lectures = teacher.lectures.order_by('-created_at')
        context = {
            'teacher': teacher,
            'lectures': lectures
        }
        return render(request, self.template_name, context)


def add_lecture(request):
    if request.method == 'POST':
        form = LectureForm(request.POST)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.lecturer = request.user
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


def lecture_detail(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    return render(request, 'lecture.html', {'lecture': lecture})


class SchedulesView(TemplateView):
    template_name = 'schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            if user.is_teacher:
                context['all_schedules'] = Schedules.objects.all()
            else:
                context['all_schedules'] = Schedules.objects.filter(course=user.course, facult=user.facult)
        return context


class AllTeachers(TemplateView):
    template_name = 'all-teachers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_teachers'] = User.objects.filter(is_teacher=True)
        return context


class PublicTeacherProfile(TemplateView):
    template_name = 'teacher-public_profile.html'

    def get(self, request, teacher_id):
        teacher = User.objects.get(id=teacher_id, is_teacher=True)
        lectures = teacher.lectures.order_by('-created_at')
        context = {
            'teacher': teacher,
            'lectures': lectures
        }
        return render(request, self.template_name, context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

