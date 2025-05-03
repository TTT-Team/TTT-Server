from django.urls import path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('/accounts/{account_id}/deposit/', views.BooksAPIList.as_view(), name='deposit'),
    # path('/accounts/{account_id}/withdraw/', views.BooksAPIList.as_view(), name='withdraw'),
    # path('/accounts/transfer/', views.BooksAPIList.as_view(), name='transfer'),
    # path('/accounts/', views.BooksAPIList.as_view(), name='deposit'),
    # path('/accounts/{account_id}/', views.BooksAPIList.as_view(), name='deposit'),
    #
    path('auth/login/', views.LoginAPIView.as_view(), name='login'),
    path('auth/logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('auth/signup/', views.SignUpAPIView.as_view(), name='signup'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)