from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ping_pong, register, telegram_auth, advertisements, advertisement, vip_ads, NewAdImageUploadAPIView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/telegram/", telegram_auth, name="telegram_auth"),
    # ####
    path("ping/", ping_pong),

    path("register/", register),

    path("advertisements/", advertisements),
    path("advertisements/<int:id>", advertisement),

    path("advertisements/vip", vip_ads),
    path("advertisements/images/new", NewAdImageUploadAPIView.as_view()),
    # path("advertisements/images/new", new_image),
]
