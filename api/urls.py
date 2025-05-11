from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.HelloAPIView.as_view(), name='hello'),
]
