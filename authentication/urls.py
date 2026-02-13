from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), # Add this line
    path('ops/', views.admin_dashboard, name='admin_dashboard'),
    path('director/', views.director_dashboard, name='director_dashboard'),
]