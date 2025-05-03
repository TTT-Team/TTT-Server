from django.urls import path, re_path
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('operation/', views.BooksAPIList.as_view(), name='books-list'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)