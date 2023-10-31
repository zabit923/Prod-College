from django.contrib import admin

from .models import User, Facult, Course, TeacherLink, Group


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'course', 'is_teacher')


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