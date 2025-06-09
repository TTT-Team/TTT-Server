from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/deposit/', views.DepositAPIView.as_view(), name='deposit'),
    path('accounts/withdraw/', views.WithdrawAPIView.as_view(), name='withdraw'),
    path('accounts/transfer/sbp/', views.TransferSBPAPIView.as_view(), name='transfer-sbp'),
    path('accounts/transfer/account/', views.TransferAccountAPIView.as_view(), name='transfer-account'),
    path('accounts/', views.BankAccountListCreateAPIView.as_view(), name='account-list'),
    path('accounts/<int:pk>/', views.BankAccountRetrieveUpdateDestroyAPIView.as_view(), name='account-detail'),

    path('auth/login/', views.LoginAPIView.as_view(), name='login'),
    path('auth/logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('auth/signup/', views.SignUpAPIView.as_view(), name='signup'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)