from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from .models import User, Facult, Course, TeacherLink, Group, PersonalTeacherLinks


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'course', 'is_teacher')
    list_filter = ('course', 'facult', 'group', 'is_teacher')
    search_fields = ('first_name', 'last_name')
    exclude = ('email', 'user_permissions', 'groups', 'date_joined', 'last_login')

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
    list_display = ('formatted_link',)

    def formatted_link(self, obj):
        return f"Ссылка {obj.title} для {obj.teacher}"

    formatted_link.short_description = 'Link'