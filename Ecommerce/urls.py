"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Root URL configuration. Each app owns its own urls.py; we just
# mount them here under a path prefix (see each app's urls.py for
# the individual routes it defines).
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),               # home, about, contact
    path('products/', include('products.urls')),  # catalog browsing
    path('accounts/', include('accounts.urls')),   # register/login/logout/verify
    path('cart/', include('cart.urls')),           # cart add/remove/view
    path('checkout/', include('checkout.urls')),   # address + Stripe payment
    path('orders/', include('orders.urls')),       # order history
]

# Only serve user-uploaded media directly from Django in development.
# In production, media is served from Cloudinary instead (see
# Ecommerce/settings.py -> USE_CLOUDINARY), and static assets are
# served via WhiteNoise, not this URLconf.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
