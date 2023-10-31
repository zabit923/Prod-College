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
from django.views.generic.detail import DetailView




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
            messages.error(request, 'Извините, попробуйте войти в аккаунт попозже')
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
            context['form'] = UserProfileForm(instance=user, initial={'facult': user.facult, 'course': user.course,
                                              'group': user.group})
        else:
            context['links'] = TeacherLink.objects.filter(faculty=user.facult, course=user.course, group=user.group)
        context['all_rpd'] = RPD.objects.filter(course=user.course, facult=user.facult)
        context['schedules'] = Schedules.objects.filter(facult=user.facult, course=user.course, group=user.group)
        return context

    def post(self, request, *args, **kwargs):
        link_form = LinkForm(request.POST)
        if link_form.is_valid():
            facult = link_form.cleaned_data['facult']
            course = link_form.cleaned_data['course']
            group = link_form.cleaned_data['group']
            link = link_form.cleaned_data['link']
            user = request.user
            existing_link = TeacherLink.objects.filter(teacher=user, faculty=facult, course=course, group=group).first()
            if existing_link:
                existing_link.link = link
                existing_link.save()
            else:
                new_link = TeacherLink(teacher=user, faculty=facult, course=course, group=group, link=link)
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
                context['all_schedules'] = Schedules.objects.filter(course=user.course, facult=user.facult)
        return context


class AllTeachers(TemplateView):
    template_name = 'all-teachers.html'

    def get(self, request, **kwargs):
        user = self.request.user
        facult = user.facult
        course = user.course
        group = user.group
        teachers = User.objects.filter(is_teacher=True)
        teachers_with_lectures = teachers.filter(lectures__facult=facult, lectures__course=course, lectures__group=group).distinct()
        context = {'all_teachers': teachers_with_lectures}
        return render(request, self.template_name, context)


class PublicTeacherProfile(TemplateView):
    template_name = 'teacher-public_profile.html'

    def get(self, request, teacher_id):
        facult = self.request.user.facult
        course = self.request.user.course
        group = self.request.user.group
        teacher = User.objects.get(id=teacher_id, is_teacher=True)
        lectures = teacher.lectures.filter(facult=facult, course=course, group=group).order_by('-created_at')
        context = {
            'teacher': teacher,
            'lectures': lectures
        }
        return render(request, self.template_name, context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

