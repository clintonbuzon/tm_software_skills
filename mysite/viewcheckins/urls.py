from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:user>/', views.filter_by_user, name='filter_by_user'),
]