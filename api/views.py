from django.contrib import messages
from django.db import models
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework import viewsets
from .models import PlatformUser, Course, Test, Question, Answer, Result, UserTheme
from .forms import UserForm, CourseForm, TestForm, QuestionForm, AnswerForm, ResultForm
#from django.contrib.auth.models import User
from django.db.models import Avg, Count, Max, Min
from django.utils import timezone
from datetime import timedelta

from .serializers import UserSerializer, CourseSerializer, TestSerializer, QuestionSerializer, AnswerSerializer, \
    ResultSerializer


# === Головна сторінка ===
def home(request):
    context = {
        'teachers_count': PlatformUser.objects.filter(role='teacher').count(),
        'students_count': PlatformUser.objects.filter(role='student').count(),
        'admins_count': PlatformUser.objects.filter(role='admin').count(),
        'users_count': PlatformUser.objects.count(),
        'courses_count': Course.objects.count(),
        'tests_count': Test.objects.count(),
        'questions_count': Question.objects.count(),
        'answers_count': Answer.objects.count(),
        'results_count': Result.objects.count(),

    }
    return render(request, 'home.html', context)

# === Users ===
class UserListView(ListView):
    model = PlatformUser
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return PlatformUser.objects.all().order_by('id')


class UserCreateView(CreateView):
    model = PlatformUser
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')


class UserUpdateView(UpdateView):
    model = PlatformUser
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')


def user_delete(request, pk):
    user = get_object_or_404(PlatformUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Користувача успішно видалено!')
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})

# === Courses ===
class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses_with_teachers'] = Course.objects.filter(teacher__isnull=False)
        return context

class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        messages.success(self.request, 'Курс успішно створено!')
        return super().form_valid(form)

class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        messages.success(self.request, 'Курс успішно оновлено!')
        return super().form_valid(form)

def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Курс успішно видалено!')
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

# === Tests ===
class TestListView(ListView):
    model = Test
    template_name = 'tests/test_list.html'
    context_object_name = 'tests'

class TestCreateView(CreateView):
    model = Test
    form_class = TestForm
    template_name = 'tests/test_form.html'
    success_url = reverse_lazy('test_list')

    def form_valid(self, form):
        messages.success(self.request, 'Тест успішно створено!')
        return super().form_valid(form)

class TestUpdateView(UpdateView):
    model = Test
    form_class = TestForm
    template_name = 'tests/test_form.html'
    success_url = reverse_lazy('test_list')

    def form_valid(self, form):
        messages.success(self.request, 'Тест успішно оновлено!')
        return super().form_valid(form)

def test_delete(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if request.method == 'POST':
        test.delete()
        messages.success(request, 'Тест успішно видалено!')
        return redirect('test_list')
    return render(request, 'tests/test_confirm_delete.html', {'test': test})

# === Questions ===
class QuestionListView(ListView):
    model = Question
    template_name = 'questions/question_list.html'
    context_object_name = 'questions'

class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'questions/question_form.html'
    success_url = reverse_lazy('question_list')

    def form_valid(self, form):
        messages.success(self.request, 'Питання успішно створено!')
        return super().form_valid(form)

class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'questions/question_form.html'
    success_url = reverse_lazy('question_list')

    def form_valid(self, form):
        messages.success(self.request, 'Питання успішно оновлено!')
        return super().form_valid(form)

def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Питання успішно видалено!')
        return redirect('question_list')
    return render(request, 'questions/question_confirm_delete.html', {'question': question})

# === Answers ===
class AnswerListView(ListView):
    model = Answer
    template_name = 'answers/answer_list.html'
    context_object_name = 'answers'

class AnswerCreateView(CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'answers/answer_form.html'
    success_url = reverse_lazy('answer_list')

    def form_valid(self, form):
        messages.success(self.request, 'Відповідь успішно створено!')
        return super().form_valid(form)

class AnswerUpdateView(UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'answers/answer_form.html'
    success_url = reverse_lazy('answer_list')

    def form_valid(self, form):
        messages.success(self.request, 'Відповідь успішно оновлено!')
        return super().form_valid(form)

def answer_delete(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if request.method == 'POST':
        answer.delete()
        messages.success(request, 'Відповідь успішно видалено!')
        return redirect('answer_list')
    return render(request, 'answers/answer_confirm_delete.html', {'answer': answer})

# === Results ===
class ResultListView(ListView):
    model = Result
    template_name = 'results/result_list.html'
    context_object_name = 'results'

class ResultCreateView(CreateView):
    model = Result
    form_class = ResultForm
    template_name = 'results/result_form.html'
    success_url = reverse_lazy('result_list')

    def form_valid(self, form):
        messages.success(self.request, 'Результат успішно створено!')
        return super().form_valid(form)

class ResultUpdateView(UpdateView):
    model = Result
    form_class = ResultForm
    template_name = 'results/result_form.html'
    success_url = reverse_lazy('result_list')

    def form_valid(self, form):
        messages.success(self.request, 'Результат успішно оновлено!')
        return super().form_valid(form)

def result_delete(request, pk):
    result = get_object_or_404(Result, pk=pk)
    if request.method == 'POST':
        result.delete()
        messages.success(request, 'Результат успішно видалено!')
        return redirect('result_list')
    return render(request, 'results/result_confirm_delete.html', {'result': result})

# === API Views ===
class UserViewSet(viewsets.ModelViewSet):
    queryset = PlatformUser.objects.all()
    serializer_class = UserSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


def documentation(request):
    """Сторінка документації системи"""

    # Дані про таблиці та зв'язки
    database_structure = {
        'platform_users': {
            'description': 'Таблиця користувачів системи',
            'fields': [
                {'name': 'id', 'type': 'INT AUTO_INCREMENT', 'description': 'Первинний ключ'},
                {'name': 'username', 'type': 'VARCHAR(50)', 'description': 'Унікальне ім\'я користувача'},
                {'name': 'email', 'type': 'VARCHAR(100)', 'description': 'Електронна пошта'},
                {'name': 'password', 'type': 'VARCHAR(255)', 'description': 'Пароль'},
                {'name': 'role', 'type': 'VARCHAR(10)', 'description': 'Роль (student/teacher/admin)'},
            ],
            'relationships': [
                '1 → ∞ courses (teacher)',
                '1 → ∞ results (user)'
            ]
        },
        'courses': {
            'description': 'Таблиця навчальних курсів',
            'fields': [
                {'name': 'course_id', 'type': 'INT AUTO_INCREMENT', 'description': 'Первинний ключ'},
                {'name': 'course_name', 'type': 'VARCHAR(100)', 'description': 'Назва курсу'},
                {'name': 'description', 'type': 'TEXT', 'description': 'Опис курсу'},
                {'name': 'teacher_id', 'type': 'INT', 'description': 'Зовнішній ключ до platform_users'},
            ],
            'relationships': [
                '∞ ← 1 platform_users (teacher)',
                '1 → ∞ tests (course)'
            ]
        },
        'tests': {
            'description': 'Таблиця тестів',
            'fields': [
                {'name': 'test_id', 'type': 'INT AUTO_INCREMENT', 'description': 'Первинний ключ'},
                {'name': 'course_id', 'type': 'INT', 'description': 'Зовнішній ключ до courses'},
                {'name': 'test_name', 'type': 'VARCHAR(100)', 'description': 'Назва тесту'},
                {'name': 'description', 'type': 'TEXT', 'description': 'Опис тесту'},
            ],
            'relationships': [
                '∞ ← 1 courses (course)',
                '1 → ∞ questions (test)',
                '1 → ∞ results (test)'
            ]
        },
        'questions': {
            'description': 'Таблиця питань до тестів',
            'fields': [
                {'name': 'question_id', 'type': 'INT AUTO_INCREMENT', 'description': 'Первинний ключ'},
                {'name': 'test_id', 'type': 'INT', 'description': 'Зовнішній ключ до tests'},
                {'name': 'question_text', 'type': 'TEXT', 'description': 'Текст питання'},
            ],
            'relationships': [
                '∞ ← 1 tests (test)',
                '1 → ∞ answers (question)'
            ]
        },
        'answers': {
            'description': 'Таблиця варіантів відповідей',
            'fields': [
                {'name': 'answer_id', 'type': 'INT AUTO_INCREMENT', 'description': 'Первинний ключ'},
                {'name': 'question_id', 'type': 'INT', 'description': 'Зовнішній ключ до questions'},
                {'name': 'answer_text', 'type': 'TEXT', 'description': 'Текст відповіді'},
                {'name': 'is_correct', 'type': 'BOOLEAN', 'description': 'Позначка правильної відповіді'},
            ],
            'relationships': [
                '∞ ← 1 questions (question)'
            ]
        },
        'results': {
            'description': 'Таблиця результатів тестувань',
            'fields': [
                {'name': 'result_id', 'type': 'INT AUTO_INCREMENT', 'description': 'Первинний ключ'},
                {'name': 'user_id', 'type': 'INT', 'description': 'Зовнішній ключ до platform_users'},
                {'name': 'test_id', 'type': 'INT', 'description': 'Зовнішній ключ до tests'},
                {'name': 'score', 'type': 'DECIMAL(5,2)', 'description': 'Оцінка у відсотках'},
                {'name': 'passed_at', 'type': 'DATETIME', 'description': 'Дата проходження'},
            ],
            'relationships': [
                '∞ ← 1 platform_users (user)',
                '∞ ← 1 tests (test)'
            ]
        }
    }

    # Опис кнопок та функціоналу
    buttons_description = {
        'home_page': [
            {'button': '👥 Керувати (Користувачі)', 'function': 'Перехід до списку користувачів'},
            {'button': '👥 Додати (Користувачі)', 'function': 'Створення нового користувача'},
            {'button': '📚 Керувати (Курси)', 'function': 'Перехід до списку курсів'},
            {'button': '📚 Додати (Курси)', 'function': 'Створення нового курсу'},
            {'button': '🧪 Керувати (Тести)', 'function': 'Перехід до списку тестів'},
            {'button': '🧪 Додати (Тести)', 'function': 'Створення нового тесту'},
            {'button': '❓ Керувати (Питання)', 'function': 'Перехід до списку питань'},
            {'button': '❓ Додати (Питання)', 'function': 'Створення нового питання'},
            {'button': '✅ Керувати (Відповіді)', 'function': 'Перехід до списку відповідей'},
            {'button': '✅ Додати (Відповіді)', 'function': 'Створення нової відповіді'},
            {'button': '📊 Керувати (Результати)', 'function': 'Перехід до списку результатів'},
            {'button': '📊 Додати (Результати)', 'function': 'Створення нового результату'},
        ],
        'list_pages': [
            {'button': '✏️', 'function': 'Редагування запису'},
            {'button': '🗑️', 'function': 'Видалення запису'},
            {'button': '➕ Додати', 'function': 'Створення нового запису'},
            {'button': '🧪 (Тести курсу)', 'function': 'Перегляд тестів курсу'},
            {'button': '📝 (Відповіді)', 'function': 'Перегляд відповідей питання'},
        ],
        'form_pages': [
            {'button': '💾 Зберегти', 'function': 'Збереження даних форми'},
            {'button': '❌ Скасувати', 'function': 'Повернення без збереження'},
        ]
    }

    # Інструкція з запуску
    installation_guide = [
        "1. Встановіть Python 3.8+ та створіть віртуальне середовище",
        "2. Встановіть залежності: pip install django mysqlclient cryptography",
        "3. Налаштуйте базу даних MySQL або використовуйте SQLite",
        "4. Виконайте міграції: python manage.py makemigrations && python manage.py migrate",
        "5. Створіть суперкористувача: python manage.py createsuperuser",
        "6. Запустіть сервер: python manage.py runserver",
        "7. Відкрийте браузер: http://127.0.0.1:8000/"
    ]

    context = {
        'database_structure': database_structure,
        'buttons_description': buttons_description,
        'installation_guide': installation_guide,
    }

    return render(request, 'documentation.html', context)


# === СТАТИСТИКА ===
def statistics(request):
    """Сторінка з детальною статистикою"""

    # Загальна статистика
    total_users = PlatformUser.objects.count()
    total_tests_taken = Result.objects.count()
    avg_score = Result.objects.aggregate(Avg('score'))['score__avg'] or 0

    # Статистика по ролям
    students = PlatformUser.objects.filter(role='student').count()
    teachers = PlatformUser.objects.filter(role='teacher').count()

    # Топ-5 студентів
    top_students = Result.objects.values('user__username').annotate(
        avg_score=Avg('score'),
        tests_count=Count('result_id')
    ).order_by('-avg_score')[:5]

    # Топ-5 тестів (найбільш складні)
    hardest_tests = Result.objects.values('test__test_name').annotate(
        avg_score=Avg('score'),
        attempts=Count('result_id')
    ).order_by('avg_score')[:5]

    # Активність за останній тиждень
    week_ago = timezone.now() - timedelta(days=7)
    recent_activity = Result.objects.filter(passed_at__gte=week_ago).count()

    # Статистика по курсах
    courses_stats = Course.objects.annotate(
        tests_count=Count('test'),
        avg_score=Avg('test__result__score')
    ).order_by('-tests_count')

    context = {
        'total_users': total_users,
        'students': students,
        'teachers': teachers,
        'total_tests_taken': total_tests_taken,
        'avg_score': round(avg_score, 2),
        'top_students': top_students,
        'hardest_tests': hardest_tests,
        'recent_activity': recent_activity,
        'courses_stats': courses_stats,
    }

    return render(request, 'statistics.html', context)


# === ПРОХОДЖЕННЯ ТЕСТУ ===
def take_test(request, test_id):
    """Інтерактивне проходження тесту"""
    test = get_object_or_404(Test, test_id=test_id)
    questions = Question.objects.filter(test=test).prefetch_related('answer_set')

    if request.method == 'POST':
        # Обробка відповідей
        score = 0
        total_questions = questions.count()
        answers_data = []

        for question in questions:
            selected_answer_id = request.POST.get(f'question_{question.question_id}')
            if selected_answer_id:
                selected_answer = Answer.objects.get(answer_id=selected_answer_id)
                is_correct = selected_answer.is_correct
                if is_correct:
                    score += 1

                answers_data.append({
                    'question_id': question.question_id,
                    'question_text': question.question_text,
                    'selected_answer': selected_answer.answer_text,
                    'is_correct': is_correct,
                    'correct_answer': Answer.objects.filter(
                        question=question,
                        is_correct=True
                    ).first().answer_text
                })

        # Підрахунок результату
        final_score = (score / total_questions * 100) if total_questions > 0 else 0

        # Збереження результату (якщо є user_id в POST)
        user_id = request.POST.get('user_id')
        if user_id:
            user = PlatformUser.objects.get(id=user_id)
            Result.objects.create(
                user=user,
                test=test,
                score=final_score,
                answers_data=answers_data
            )

        # Показуємо результати
        return render(request, 'tests/test_result.html', {
            'test': test,
            'score': final_score,
            'correct_answers': score,
            'total_questions': total_questions,
            'answers_data': answers_data
        })

    # GET запит - показуємо тест
    users = PlatformUser.objects.filter(role='student')
    return render(request, 'tests/take_test.html', {
        'test': test,
        'questions': questions,
        'users': users
    })


def test_results_detail(request, result_id):
    """Детальний перегляд результату тесту"""
    result = get_object_or_404(Result, result_id=result_id)

    context = {
        'result': result,
        'answers_data': result.answers_data or []
    }

    return render(request, 'tests/result_detail.html', context)

# === Top Results ===
def top_results(request):
    # Топ-5 студентів за останні 7 днів
    week_ago = timezone.now() - timezone.timedelta(days=7)

    top_students = Result.objects.filter(
        passed_at__gte=week_ago,
        user__role='student'
    ).values(
        'user__username',
        'user__id'
    ).annotate(
        avg_score=models.Avg('score'),
        tests_count=models.Count('test')
    ).order_by('-avg_score')[:5]

    context = {
        'top_students': top_students,
        'week_ago': week_ago.date()
    }
    return render(request, 'top_results/top_results.html', context)


# === Theme Selection ===
def theme_selection(request):
    if request.method == 'POST':
        theme = request.POST.get('theme', 'light')

        # Зберігаємо в сесії для всіх користувачів
        request.session['theme'] = theme
        request.session.modified = True

        # Для авторизованих користувачів зберігаємо в базі
        if request.user.is_authenticated and hasattr(request.user, 'platformuser'):
            user_theme, created = UserTheme.objects.get_or_create(
                user=request.user.platformuser
            )
            user_theme.theme = theme
            user_theme.save()

        messages.success(request, f'Тему змінено на {"світлу" if theme == "light" else "темну"}!')
        return redirect('theme_selection')

    # Для GET запиту просто показуємо сторінку
    return render(request, 'themes/theme_selection.html')


# Додати context processor для теми
def theme_context(request):
    current_theme = 'light'
    if request.user.is_authenticated and hasattr(request.user, 'platformuser'):
        try:
            user_theme = UserTheme.objects.get(user=request.user.platformuser)
            current_theme = user_theme.theme
        except UserTheme.DoesNotExist:
            pass
    else:
        current_theme = request.session.get('theme', 'light')

    return {'current_theme': current_theme}
