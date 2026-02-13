from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'), # Ensure there's no slash if your action doesn't have one
    path('ops/', views.admin_dashboard, name='admin_dashboard'),
    path('director/', views.director_dashboard, name='director_dashboard'),
    


]