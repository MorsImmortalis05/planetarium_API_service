from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, \
    SpectacularRedocView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path('admin/', admin.site.urls),
    path("api/doc/", SpectacularAPIView.as_view(), name="schema"),
    path("api/doc/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/doc/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/planetarium/",
         include("planetarium.urls", namespace="planetarium")),
    path("api/user/", include("user.urls", namespace="user")),
]
