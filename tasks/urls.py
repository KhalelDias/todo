from django.urls import path
from .views import TasksList, TasksDetail, mark_done

urlpatterns = [
    path('', TasksList.as_view()),
    path('<int:pk>/', TasksDetail.as_view()),
    path('<int:pk>/execute', mark_done),
]
