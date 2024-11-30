from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path('index', views.index, name='index'),
    path('volunteers/', views.get_volunteers, name='get_volunteers'),
    path('markers/', views.get_markers, name='get_markers'),
    path('save-location/', views.save_location, name='save_location'),
    path('get-user-locations/', views.get_active_user_locations, name='get_user_locations'),
]
