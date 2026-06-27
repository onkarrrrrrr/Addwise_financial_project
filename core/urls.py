from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from leads import views as leads_views

urlpatterns = [
    # Django admin moved to a non-obvious path to prevent brute-force attacks
    path('oldsuperadmin/', admin.site.urls),
    # Honeypot: infinite-loading decoy for any /admin/* requests
    path('admin/', leads_views.admin_honeypot_view),
    re_path(r'^admin/.*$', leads_views.admin_honeypot_view),
    # All lead/site routes
    path('', include('leads.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)