from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CompanyViewSet, CustomUserViewSet, LogoutView,
                    RetrieveOwnUserDataView)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'users', CustomUserViewSet)


urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('', include(router.urls)),
    path('dev-auth/', include("rest_framework.urls")),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('me/', RetrieveOwnUserDataView.as_view(), name='retrieve-own-data'),
    path('registration/', include('dj_rest_auth.registration.urls')),
]
