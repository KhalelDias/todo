from django.urls import path
from .views import TestResponseView

urlpatterns = [
    path('', TestResponseView.as_view())
]