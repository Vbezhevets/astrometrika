from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('robots.txt', RedirectView.as_view(url='/static/robots.txt', permanent=True)),
]

urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
)

urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT
)
