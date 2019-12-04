from django.urls import path

from . import views

app_name = 'booking'
urlpatterns = [
    path('cruises', views.CruisesAPI.as_view(), name='cruises'),
    path('hotels', views.HotelsAPI.as_view(), name='hotels'),
]