from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView

urlpatterns = [
    path("", include("home.urls")),
    path('admin/', admin.site.urls),
    path('shop', include('shop.urls')),  # shop app er URLs
    path('users/', include('users.urls')),
    path('contact/', include('contact.urls')),
]

handler404 = "django.views.defaults.page_not_found"
handler500 = "django.views.defaults.server_error"

