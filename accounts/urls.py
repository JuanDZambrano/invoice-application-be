from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CompanyViewSet, CustomUserViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'users', CustomUserViewSet)


urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('dev-auth/', include("rest_framework.urls")),
    path('', include(router.urls)),
]
