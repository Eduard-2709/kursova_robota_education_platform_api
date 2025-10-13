# 🎯 Детальний звіт архітектури Django проекту

## 📦 Додаток: Api

### 📊 Моделі бази даних:
#### PlatformUser
- **Кількість полів:** 5
- **Основні поля:**
  - `id (AutoField)`
  - `username (CharField)`
  - `email (CharField)`
  - `password (CharField)`
  - `role (CharField)`

#### Course
- **Кількість полів:** 4
- **Основні поля:**
  - `course_id (AutoField)`
  - `course_name (CharField)`
  - `description (TextField)`
  - `teacher (ForeignKey)`

#### Test
- **Кількість полів:** 4
- **Основні поля:**
  - `test_id (AutoField)`
  - `course (ForeignKey)`
  - `test_name (CharField)`
  - `description (TextField)`

#### Question
- **Кількість полів:** 3
- **Основні поля:**
  - `question_id (AutoField)`
  - `test (ForeignKey)`
  - `question_text (TextField)`

#### Answer
- **Кількість полів:** 4
- **Основні поля:**
  - `answer_id (AutoField)`
  - `question (ForeignKey)`
  - `answer_text (TextField)`
  - `is_correct (BooleanField)`

#### Result
- **Кількість полів:** 7
- **Основні поля:**
  - `result_id (AutoField)`
  - `user (ForeignKey)`
  - `test (ForeignKey)`
  - `score (DecimalField)`
  - `passed_at (DateTimeField)`
  - `time_spent (IntegerField)`

#### UserTheme
- **Кількість полів:** 3
- **Основні поля:**
  - `id (BigAutoField)`
  - `user (OneToOneField)`
  - `theme (CharField)`

### 🎯 Views (Контролери):
- `AnswerCreateView`
- `AnswerListView`
- `AnswerUpdateView`
- `AnswerViewSet`
- `CourseCreateView`
- `CourseListView`
- `CourseUpdateView`
- `CourseViewSet`
- `CreateView`
- `DeleteView`
- `ListView`
- `QuestionCreateView`
- `QuestionListView`
- `QuestionUpdateView`
- `QuestionViewSet`
- `ResultCreateView`
- `ResultListView`
- `ResultUpdateView`
- `ResultViewSet`
- `TestCreateView`
- `TestListView`
- `TestUpdateView`
- `TestViewSet`
- `UpdateView`
- `UserCreateView`
- `UserListView`
- `UserUpdateView`
- `UserViewSet`
- `test_results_detail`

---

## 📦 Додаток: Django REST framework

### 🎯 Views (Контролери):
- `APIView`
- `View`
- `get_view_description`
- `get_view_name`

### 📄 Шаблони:
#### admin.html
- **Включає компоненти:**
  - `rest_framework/admin/list.html`
  - `rest_framework/admin/detail.html`
- **Блоки:**
  - `head `
  - `meta `
  - `title `
  - `style `
  - `bootstrap_theme `
  - `body `
  - `bodyclass `
  - `navbar `
  - `bootstrap_navbar_variant `
  - `branding `
  - `userlinks `
  - `breadcrumbs `
  - `description `
  - `script `

#### api.html
- **Наслідує:** `rest_framework/base.html`

#### base.html
- **Включає компоненти:**
  - `rest_framework/raw_data_form.html`
  - `rest_framework/raw_data_form.html`
- **Блоки:**
  - `head `
  - `meta `
  - `title `
  - `style `
  - `bootstrap_theme `
  - `body `
  - `bodyclass `
  - `navbar `
  - `bootstrap_navbar_variant `
  - `branding `
  - `userlinks `
  - `breadcrumbs `
  - `breadcrumbs_empty `
  - `content `
  - `request_forms `
  - `description `
  - `script `

#### login.html
- **Наслідує:** `rest_framework/login_base.html`

#### login_base.html
- **Наслідує:** `rest_framework/base.html`
- **Блоки:**
  - `body `
  - `branding `

#### raw_data_form.html

---

## 📦 Додаток: Django Extensions

---

## 📈 Загальна статистика проекту

- **Кількість додатків:** 3
- **Загальна кількість моделей:** 7
- **Загальна кількість views:** 33
- **Загальна кількість шаблонів:** 6
