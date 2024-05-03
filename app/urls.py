from django.urls import path
from app.views import *
from django.conf.urls.static import static
# i also want to add rought method here in URLS
urlpatterns = [
path('register/', RegisterView.as_view(), name="register"),
path('login/', LoginView.as_view(), name="LoginView"),
]
if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  