from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ping_pong, register, advertisements, ad_images

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # ####
    path("ping/", ping_pong),

    path("register/", register),
    path("register/telegram/", register),
    path("advertisements/", advertisements),
    path("advertisements/<int:id>/images", ad_images),
    # path("advertisements/<int:id>/images", FileUploadAPIView.as_view()),
]
