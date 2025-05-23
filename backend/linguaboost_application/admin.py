""" Django admin panel settings """

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import Group
from .models import (CustomUser, WebsiteInformation, Course, Lesson, OneManyTask, FixSentenceTask, TranslateWordTask,
                     SequenceTask, AccordanceTask, AccordanceTaskVariant, StudentApplication, StudentCourse,
                     DiscussionExercise, ReadingExercise, ListeningExercise, VocabularyExercise, VocabularyWord, RulesExercise,
                     LessonTestResult, CourseFinalTestResult)

admin.site.unregister(Group)


@admin.register(CustomUser)
class UserAdmin(auth_admin.UserAdmin):
    model = CustomUser
    change_password_form = auth_admin.AdminPasswordChangeForm

    list_display = ['username', 'account_type', 'email', 'phone_number', 'first_name', 'last_name', 'patronymic',
                    'is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'phone_number', 'first_name', 'last_name', 'patronymic']
    readonly_fields = ('last_login', 'date_joined',)
    list_filter = ['is_active', 'is_staff', 'is_superuser']

    ordering = ['-is_superuser']

    fieldsets = (('Personal info', {'fields': ('username', 'image', 'first_name', 'last_name', 'patronymic', 'account_type', 'birthday',
                                               'phone_number', 'email', 'password',)}),
                 ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
                 ('Important dates', {'fields': ('date_joined', 'last_login')}))

    def get_queryset(self, request):
        if request.user.account_type == 'Адміністратор':
            queryset = CustomUser.objects
            return queryset


admin.site.register(WebsiteInformation)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(OneManyTask)
admin.site.register(FixSentenceTask)
admin.site.register(TranslateWordTask)
admin.site.register(SequenceTask)
admin.site.register(AccordanceTask)
admin.site.register(AccordanceTaskVariant)
admin.site.register(StudentApplication)
admin.site.register(StudentCourse)
admin.site.register(DiscussionExercise)
admin.site.register(ReadingExercise)
admin.site.register(ListeningExercise)
admin.site.register(VocabularyExercise)
admin.site.register(VocabularyWord)
admin.site.register(RulesExercise)
admin.site.register(LessonTestResult)
admin.site.register(CourseFinalTestResult)
