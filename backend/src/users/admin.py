from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from .models import User, Facult, Course, TeacherLink, Group, PersonalTeacherLinks


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'course', 'is_teacher', 'is_graduate')
    list_filter = ('course', 'facult', 'group', 'is_teacher', 'is_graduate')
    search_fields = ('first_name', 'last_name')
    exclude = ('email', 'user_permissions', 'groups', 'date_joined', 'last_login', 'password', 'username')
    actions = ['mark_as_graduate', 'promote_course']

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        search_term = search_term.strip()
        if search_term:
            search_term_list = search_term.split()
            search_condition = Q()
            for term in search_term_list:
                search_condition |= Q(first_name__icontains=term)
                search_condition |= Q(last_name__icontains=term)
            queryset |= self.model.objects.filter(search_condition)
        return queryset, use_distinct

    @admin.action(description='Отметить как выпускников и удалить курс')
    def mark_as_graduate(self, request, queryset):
        updated_count = queryset.update(is_graduate=True, course=None)
        self.message_user(request, f'{updated_count} студентов отмечены как выпускники и у них удален курс.')

    @admin.action(description='Повысить курс для выбранных студентов')
    def promote_course(self, request, queryset):
        for student in queryset.filter(is_graduate=False):
            if student.course:
                try:
                    current_course_number = int(student.course.name)
                    new_course = Course.objects.get(name=str(current_course_number + 1))
                    student.course = new_course
                    student.save()
                except Course.DoesNotExist:
                    continue
        self.message_user(request, 'Выбранным студентам успешно повышен курс.')


@admin.register(Facult)
class FacultAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(TeacherLink)
class TeacherLinkAdmin(admin.ModelAdmin):
    list_display = ('formatted_link', 'course')

    def formatted_link(self, obj):
        return f"Ссылка для {obj.course} от {obj.teacher}"

    formatted_link.short_description = 'Link'


@admin.register(PersonalTeacherLinks)
class PersonalLink(admin.ModelAdmin):
    list_display = ('formatted_link', 'private')

    def formatted_link(self, obj):
        return f"Ссылка {obj.title} для {obj.teacher}"

    formatted_link.short_description = 'Link'
