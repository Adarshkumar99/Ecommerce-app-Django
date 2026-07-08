from django.urls import path, include
from . import views

# Checkout flow: address capture -> Stripe payment session -> success/
# cancel landing pages. `webhook/` is called server-to-server by
# Stripe itself, not by the browser (see views.stripe_webhook).
urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('payment/', views.create_checkout_session, name='payment'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]
