from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/telegram/", views.TelegramAuth.as_view(), name="telegram_auth"),
    # ####
    path("ping/", views.ping_pong),

    path("register/", views.Register.as_view()),

    path("sections/", views.Sections.as_view()),

    path("advertisements/", views.AdvertisementList.as_view()),
    path("advertisements/<int:pk>", views.AdvertisementDetail.as_view()),
    path("advertisements/images/new", views.NewAdImageUploadAPIView.as_view()),

    # path("vendor/<int:pk>"),
    path("vendor/<int:pk>/advertisements", views.VendorAdvertisementList.as_view()),
]
