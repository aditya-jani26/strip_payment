from django.urls import path
from app.views import *
from django.conf.urls.static import static
# i also want to add rought method here in URLS
urlpatterns = [
path('register/', RegisterView.as_view(), name="register"),
path('login/', LoginView.as_view(), name="LoginView"),
path('wallet-info/', WalletInfoAPIView.as_view(), name='wallet_info'),
path('create-payment-intent/', CreatePaymentIntentAPIView.as_view(), name='create_payment_intent'),
path('save-payment-method/', SavePaymentMethodAPIView.as_view(), name='save_payment_method'),
]
if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  