from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Leads app (nayi website) ko direct home page par set kar diya hai
    path('', include('leads.urls')), 
]