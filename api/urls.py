from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('documentation/', views.documentation, name='documentation'),

    # Users URLs
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/add/', views.UserCreateView.as_view(), name='user_add'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    # Courses URLs
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/add/', views.CourseCreateView.as_view(), name='course_add'),
    path('courses/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # Tests URLs
    path('tests/', views.TestListView.as_view(), name='test_list'),
    path('tests/add/', views.TestCreateView.as_view(), name='test_add'),
    path('tests/<int:pk>/edit/', views.TestUpdateView.as_view(), name='test_edit'),
    path('tests/<int:pk>/delete/', views.test_delete, name='test_delete'),

    # Questions URLs
    path('questions/', views.QuestionListView.as_view(), name='question_list'),
    path('questions/add/', views.QuestionCreateView.as_view(), name='question_add'),
    path('questions/<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='question_edit'),
    path('questions/<int:pk>/delete/', views.question_delete, name='question_delete'),

    # Answers URLs
    path('answers/', views.AnswerListView.as_view(), name='answer_list'),
    path('answers/add/', views.AnswerCreateView.as_view(), name='answer_add'),
    path('answers/<int:pk>/edit/', views.AnswerUpdateView.as_view(), name='answer_edit'),
    path('answers/<int:pk>/delete/', views.answer_delete, name='answer_delete'),

    # Results URLs
    path('results/', views.ResultListView.as_view(), name='result_list'),
    path('results/add/', views.ResultCreateView.as_view(), name='result_add'),
    path('results/<int:pk>/edit/', views.ResultUpdateView.as_view(), name='result_edit'),
    path('results/<int:pk>/delete/', views.result_delete, name='result_delete'),
    path('statistics/', views.statistics, name='statistics'),
    path('tests/<int:test_id>/take/', views.take_test, name='take_test'),
    path('results/<int:result_id>/detail/', views.test_results_detail, name='result_detail'),

    path('top-results/', views.top_results, name='top_results'),
    path('themes/', views.theme_selection, name='theme_selection'),
]