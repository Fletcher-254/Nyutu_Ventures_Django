from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendor_list, name='vendor_list'),
    path('create/', views.vendor_create, name='vendor_create'),
    path('<int:pk>/', views.vendor_detail, name='vendor_detail'),
    path('unpaid/', views.unpaid_vendors, name='unpaid_vendors'),
    path('<int:pk>/pay/', views.record_payment, name='record_payment'),
    path('payment/<int:vendor_id>/', views.record_payment, name='record_payment')
]