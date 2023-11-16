from django.contrib import auth, messages
from django.db.models import Q
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView

from .forms import UserLoginForm, UserProfileForm, LectureForm, LinkForm, PersonalLinkForm, ReviewForm
from .models import User, TeacherLink, PersonalTeacherLinks
from lessons.models import Lecture, Schedules, RPD, ProfDB, Reviews
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView




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


def add_review(request, pk):
    lecture = get_object_or_404(Lecture, id=pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            name = request.user
            text = form.cleaned_data['text']
            review = Reviews(name=name, text=text, lecture=lecture)
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


class AllTeachers(TemplateView):
    template_name = 'all-teachers.html'

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
    template_name = 'teacher-profile.html'
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
    template_name = 'teacher-public_profile.html'
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

