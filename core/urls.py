from django.contrib import admin
from django.urls import path, include
from authentication.views import login_view, logout_view, director_dashboard, admin_dashboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    
    path('', login_view, name='login'), 
    path('logout/', logout_view, name='logout'),
    
    
    path('dashboard/executive/', director_dashboard, name='director_dashboard'),
    path('dashboard/ops/', admin_dashboard, name='admin_dashboard'),
    
    
    path('employees/', include('employees.urls')),
    path('vehicles/', include('vehicles.urls')),
    path('expense/', include('expenses.urls')),
    path('vendors/', include('vendors.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)