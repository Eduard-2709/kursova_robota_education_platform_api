# admin.py
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import PlatformUser, Course, Test, Question, Answer, Result, UserTheme


class PlatformUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'get_courses_count')
    list_filter = ('role',)
    search_fields = ('username', 'email')
    ordering = ('id',)

    # Автоматичне хешування пароля при збереженні
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

    def get_courses_count(self, obj):
        return obj.course_set.count()

    get_courses_count.short_description = 'Кількість курсів'


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'course_name', 'teacher', 'get_tests_count')
    list_filter = ('teacher__role',)
    search_fields = ('course_name', 'teacher__username')
    raw_id_fields = ('teacher',)

    def get_tests_count(self, obj):
        return obj.test_set.count()

    get_tests_count.short_description = 'Кількість тестів'


class TestAdmin(admin.ModelAdmin):
    list_display = ('test_id', 'test_name', 'course', 'get_questions_count')
    list_filter = ('course',)
    search_fields = ('test_name', 'course__course_name')

    def get_questions_count(self, obj):
        return obj.question_set.count()

    get_questions_count.short_description = 'Кількість питань'


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    fields = ('answer_text', 'is_correct')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'test', 'question_text_preview')
    list_filter = ('test',)
    search_fields = ('question_text', 'test__test_name')
    inlines = [AnswerInline]

    def question_text_preview(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text

    question_text_preview.short_description = 'Текст питання'


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_id', 'question', 'answer_text_preview', 'is_correct')
    list_filter = ('is_correct', 'question__test')
    search_fields = ('answer_text', 'question__question_text')

    def answer_text_preview(self, obj):
        return obj.answer_text[:50] + '...' if len(obj.answer_text) > 50 else obj.answer_text

    answer_text_preview.short_description = 'Відповідь'


class ResultAdmin(admin.ModelAdmin):
    list_display = ('result_id', 'user', 'test', 'score', 'passed_at', 'time_spent')
    list_filter = ('test', 'passed_at')
    search_fields = ('user__username', 'test__test_name')
    readonly_fields = ('passed_at',)
    date_hierarchy = 'passed_at'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'test')


class UserThemeAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme')
    list_filter = ('theme',)
    search_fields = ('user__username',)


# Реєстрація моделей в адмін-панелі
admin.site.register(PlatformUser, PlatformUserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(UserTheme, UserThemeAdmin)

# Кастомізація заголовка адмін-панелі
admin.site.site_header = "Education Platform Administration"
admin.site.site_title = "Education Platform Admin"
admin.site.index_title = "Welcome to Education Platform Admin Panel"