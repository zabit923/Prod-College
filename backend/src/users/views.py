from django.contrib import auth, messages
from django.db.models import Q
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView

from .forms import UserLoginForm, UserProfileForm, LinkForm, PersonalLinkForm
from .models import User, TeacherLink, PersonalTeacherLinks
from django.shortcuts import get_object_or_404

from lessons.forms import ReviewForm
from lessons.models import Schedules, Lecture, ProfDB


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        first_name: str = request.POST['first_name']
        last_name: str = request.POST['last_name']
        student_id = request.POST['student_id']
        user = auth.authenticate(first_name=first_name.title().strip(), last_name=last_name.title().strip(), student_id=student_id)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('users:profile', args=[request.user.pk]))
        else:
            messages.error(request, 'Извините, попробуйте войти в аккаунт попозже')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'login/login.html', context)


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'pages/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_teacher:
            context['form'] = UserProfileForm(instance=user, initial={'facult': user.facult, 'course': user.course,
                                              'group': user.group})
            context['personal_links'] = PersonalTeacherLinks.objects.filter(teacher=user, private=False).order_by('-created_at')
            context['private_personal_links'] = PersonalTeacherLinks.objects.filter(teacher=user, private=True).order_by('-created_at')
            context['links'] = TeacherLink.objects.filter(teacher=user).order_by('-created_at')

            context['ur_teachers'] = User.objects.filter(
                Q(lectures__lecturer=user, lectures__facult=4) | Q(personalteacherlinks__teacher=user, personalteacherlinks__facult=4) |
                Q(lectures__lecturer=user, lectures__facult=5) | Q(personalteacherlinks__teacher=user, personalteacherlinks__facult=5) |
                Q(lectures__lecturer=user, lectures__facult=6) | Q(personalteacherlinks__teacher=user, personalteacherlinks__facult=6)
            ).distinct()
        else:
            context['prof_db'] = ProfDB.objects.filter(facult=user.facult)
            context['links'] = TeacherLink.objects.filter(
                Q(faculty=user.facult, course=user.course, group=user.group) | Q(faculty=user.facult, course=user.course, group=None)
            ).order_by('-created_at')
        context['schedules'] = Schedules.objects.filter(facult=user.facult)
        return context

    def post(self, request, *args, **kwargs):
        link_form = LinkForm(request.POST)
        if link_form.is_valid():
            facult = link_form.cleaned_data['facult']
            course = link_form.cleaned_data['course']
            group = link_form.cleaned_data['group']
            link = link_form.cleaned_data['link']
            user = request.user
            new_link = TeacherLink(teacher=user, faculty=facult, course=course, group=group, link=link)
            new_link.save()

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


def add_personal_link(request):
    if request.method == 'POST':
        form = PersonalLinkForm(request.POST)
        if form.is_valid():
            teacher = request.user
            title = form.cleaned_data['title']
            link = form.cleaned_data['link']
            facult = form.cleaned_data['facult']
            course = form.cleaned_data['course']
            group = form.cleaned_data['group'] if 'group' in form.cleaned_data else None
            private = form.cleaned_data['private']
            personal_link = PersonalTeacherLinks(teacher=teacher, title=title,
                                                 link=link, facult=facult,
                                                 course=course, group=group, private=private)
            personal_link.save()
            return redirect('users:profile', pk=teacher.pk)


def delete_personal_link(request, link_id):
    link = get_object_or_404(PersonalTeacherLinks, pk=link_id)
    if link.teacher == request.user:
        link.delete()
        messages.success(request, 'Ссылка успешно удалена.')
    else:
        messages.error(request, 'Вы не можете удалить эту ссылку.')

    teacher_id = request.user.pk
    profile_url = reverse('users:profile', args=(teacher_id,))
    return redirect(profile_url)


def delete_link(request, link_id):
    message = get_object_or_404(TeacherLink, pk=link_id)
    if message.teacher == request.user:
        message.delete()
        messages.success(request, 'Ссылка успешно удалена.')
    else:
        messages.error(request, 'Вы не можете удалить эту ссылку.')

    teacher_id = request.user.pk
    profile_url = reverse('users:profile', args=(teacher_id,))
    return redirect(profile_url)


class AllTeachers(TemplateView):
    template_name = 'pages/all-teachers.html'

    def get(self, request, **kwargs):
        user = self.request.user
        facult = user.facult
        course = user.course
        group = user.group
        teachers = User.objects.filter(is_teacher=True)

        teachers_with_lectures = teachers.filter(
            Q(lectures__facult=facult, lectures__course=course, lectures__group=group) |
            Q(lectures__facult=facult, lectures__course=course, lectures__group=None) |
            Q(personalteacherlinks__facult=facult, personalteacherlinks__course=course, personalteacherlinks__group=group) |
            Q(personalteacherlinks__facult=facult, personalteacherlinks__course=course, personalteacherlinks__group=None)
        ).distinct()
        context = {'all_teachers': teachers_with_lectures}
        return render(request, self.template_name, context)


class TeacherProfile(TemplateView):
    template_name = 'pages/teacher-profile.html'
    form = ReviewForm()

    def get(self, request, teacher_id):
        teacher = User.objects.get(id=teacher_id, is_teacher=True)
        lectures = teacher.lectures.order_by('-created_at')
        context = {
            'teacher': teacher,
            'lectures': lectures,
            'form': self.form
        }
        return render(request, self.template_name, context)


class PublicTeacherProfile(TemplateView):
    template_name = 'pages/teacher-public_profile.html'
    form = ReviewForm()

    def get(self, request, teacher_id):
        facult = self.request.user.facult
        course = self.request.user.course
        group = self.request.user.group
        teacher = User.objects.get(id=teacher_id, is_teacher=True)
        lectures = Lecture.objects.filter(
            Q(lecturer=teacher, facult=facult, course=course, group=group) | Q(lecturer=teacher, facult=facult,
                                                                               course=course, group=None)
        ).order_by('-created_at')

        personal_links = PersonalTeacherLinks.objects.filter(
            Q(teacher=teacher, facult=facult, course=course, group=group) | Q(teacher=teacher, facult=facult,
                                                                              course=course, group=None)
        ).order_by('-created_at')

        context = {
            'teacher': teacher,
            'lectures': lectures,
            'personal_links': personal_links,
            'form': self.form
        }
        return render(request, self.template_name, context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
