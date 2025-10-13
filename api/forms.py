from django import forms
from .models import PlatformUser, Course, Test, Question, Answer, Result, UserTheme


class UserForm(forms.ModelForm):
    class Meta:
        model = PlatformUser
        fields = ['username', 'email', 'role']

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = PlatformUser.objects.exclude(pk=self.instance.pk) if self.instance.pk else PlatformUser.objects.all()
        if qs.filter(username=username).exists():
            raise forms.ValidationError("Користувач з таким ім'ям вже існує")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = PlatformUser.objects.exclude(pk=self.instance.pk) if self.instance.pk else PlatformUser.objects.all()
        if qs.filter(email=email).exists():
            raise forms.ValidationError("Користувач з таким email вже існує")
        return email

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'description', 'teacher']
        widgets = {
            'course_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть назву курсу'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть опис курсу',
                'rows': 4
            }),
            'teacher': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Обмежуємо вибір викладача
        self.fields['teacher'].queryset = PlatformUser.objects.filter(role__in=['teacher', 'admin'])  # ЗМІНА
        self.fields['teacher'].label = "Викладач"
        self.fields['course_name'].label = "Назва курсу"
        self.fields['description'].label = "Опис курсу"
        self.fields['teacher'].required = False


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['course', 'test_name', 'description']
        widgets = {
            'course': forms.Select(attrs={
                'class': 'form-control'
            }),
            'test_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть назву тесту'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть опис тесту',
                'rows': 4
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].label = "Курс"
        self.fields['test_name'].label = "Назва тесту"
        self.fields['description'].label = "Опис тесту"


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['test', 'question_text']
        widgets = {
            'test': forms.Select(attrs={
                'class': 'form-control'
            }),
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть текст питання',
                'rows': 4
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['test'].label = "Тест"
        self.fields['question_text'].label = "Текст питання"


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question', 'answer_text', 'is_correct']
        widgets = {
            'question': forms.Select(attrs={
                'class': 'form-control'
            }),
            'answer_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть текст відповіді',
                'rows': 3
            }),
            'is_correct': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].label = "Питання"
        self.fields['answer_text'].label = "Текст відповіді"
        self.fields['is_correct'].label = "Правильна відповідь"


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['user', 'test', 'score']
        widgets = {
            'user': forms.Select(attrs={
                'class': 'form-control'
            }),
            'test': forms.Select(attrs={
                'class': 'form-control'
            }),
            'score': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': '0.00'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].label = "Користувач"
        self.fields['test'].label = "Тест"
        self.fields['score'].label = "Оцінка (%)"

        # Обмежуємо вибір користувача тільки студентами
        self.fields['user'].queryset = PlatformUser.objects.filter(role='student')

class ThemeForm(forms.ModelForm):
    class Meta:
        model = UserTheme
        fields = ['theme']
        widgets = {
            'theme': forms.Select(attrs={
                'class': 'form-control'
            })
        }
