from django.urls import path

from . import views

app_name = 'booking'
urlpatterns = [
    path('api/hotels', views.HotelsAPI.as_view(), name='hotels'),
]