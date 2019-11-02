from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:user>/', views.filter_by_user, name='filter_by_user'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)