from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('robots.txt', RedirectView.as_view(url='/static/robots.txt', permanent=True)),

    path('stripe-webhook/', core_views.stripe_webhook, name='stripe_webhook'),
]

urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
)

if settings.DEBUG is False:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )