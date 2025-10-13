from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api import views

# API Router
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'tests', views.TestViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'results', views.ResultViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # API endpoints
    path('', include('api.urls')),       # UI endpoints
]

#router.register(r'users', views.UserViewSet)
#router.register(r'courses', views.CourseViewSet)
#router.register(r'tests', views.TestViewSet)
#outer.register(r'questions', views.QuestionViewSet)
#outer.register(r'answers', views.AnswerViewSet)
#router.register(r'results', views.ResultViewSet)