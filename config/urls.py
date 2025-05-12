 
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), 
    path('robots.txt', RedirectView.as_view(url='/static/robots.txt', permanent=True)),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT
)