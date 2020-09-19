from django.urls import path
from .views import TasksList, TasksDetail

urlpatterns = [
    path('', TasksList.as_view()),
    path('<int:pk>/', TasksDetail.as_view()),
]
