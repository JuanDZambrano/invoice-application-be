from django.contrib import admin
from django.urls import (include, path)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('invoice_app.urls')),
    path('reports/', include('reports.urls')),
]
