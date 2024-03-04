from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ping_pong, register, telegram_auth, advertisements, ad_images

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/telegram/", telegram_auth, name="telegram_auth"),
    # ####
    path("ping/", ping_pong),

    path("register/", register),
    path("advertisements/", advertisements),
    path("advertisements/<int:id>/images", ad_images),
    # path("advertisements/<int:id>/images", FileUploadAPIView.as_view()),
]
