from django.db import models

class PlatformUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=[
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin')
    ], default='student')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'platform_users'

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    teacher = models.ForeignKey('PlatformUser', on_delete=models.SET_NULL, null=True)  # Важливо: 'PlatformUser'

    def __str__(self):
        return self.course_name

    class Meta:
        db_table = 'courses'

class Test(models.Model):
    test_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.test_name

    class Meta:
        db_table = 'tests'

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question_text = models.TextField()

    def __str__(self):
        return f"Question {self.question_id}"

    class Meta:
        db_table = 'questions'

class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer {self.answer_id}"

    class Meta:
        db_table = 'answers'

class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(PlatformUser, on_delete=models.CASCADE)
    test = models.ForeignKey('Test', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    passed_at = models.DateTimeField(auto_now_add=True)
    time_spent = models.IntegerField(null=True, blank=True, help_text="Час у секундах")  # НОВЕ
    answers_data = models.JSONField(null=True, blank=True)  # НОВЕ - зберігає детальні відповіді

    def __str__(self):
        return f"Result {self.result_id}"

    class Meta:
        db_table = 'results'

class UserTheme(models.Model):
    user = models.OneToOneField(PlatformUser, on_delete=models.CASCADE)
    theme = models.CharField(max_length=10, choices=[
        ('light', 'Світла'),
        ('dark', 'Темна')
    ], default='light')

    def __str__(self):
        return f"{self.user.username} - {self.theme}"

    class Meta:
        db_table = 'user_themes'
