# from django.core.cache import cache
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language, activate, gettext
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
# from rest_framework.mixins import RetrieveModelMixin
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Advertisement, AdImage, Section
from .serializers import UserSerializer, TelegramUserSerializer, AdvertisementSerializer, AdImageSerializer, SectionSerializer

from core.utility import log

def custom404(request, exception=None):
    return JsonResponse(
        {"status_code": 404, "detail": "The resourse was not found"}, status=404
    )

def translate(text, language):
    curr_language = get_language()
    try:
        activate(language)
        text = gettext(text)
    finally:
        activate(curr_language)
    return text


@api_view(["GET"])
@permission_classes([AllowAny])
def ping_pong(request):
    text = 'hello'
    trans = translate(text, language='uz')
    return Response("pong " + trans, status=status.HTTP_200_OK)


#
class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"success": "user has been succesfully created"},
            status=status.HTTP_201_CREATED,
        )


"""
{
    "first_name": "John",
    "last_name": "Doe",
    "phone": "901558090",
    "password": "1234"
}
"""

class TelegramAuth(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TelegramUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refreshToken": str(refresh),
                "accessToken": str(refresh.access_token)
            },
            status=status.HTTP_200_OK,
        )

"""
{
  "id": 992519627,
  "hash": "faa98f1c8c6c25d0db9b27392cf24e1fa2f9822194024bd2d786a594765cefa9",
  "first_name": "Nick",
  "last_name": "Wild",
  "username": "NickPhilomath",
  "auth_date": 1709487049,
  "photo_url":
    "https://t.me/i/userpic/320/Sn5-VT8K0XDt-4JjI5sLB_gv3u0Ew5R0ad04INgSfKo.jpg"
}
"""


class Sections(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        sections = Section.objects.prefetch_related('section_category').all()
        serializer = SectionSerializer(sections, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    


class AdvertisementList(ListCreateAPIView):
    # permission_classes = [AllowAny]
    queryset = Advertisement.objects.prefetch_related('ad_images').filter(is_active=True)
    serializer_class = AdvertisementSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_context(self):
        return {'user': self.request.user}


class AdvertisementDetail(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Advertisement.objects.prefetch_related('ad_images').filter(is_active=True)
    serializer_class = AdvertisementSerializer


class VendorAdvertisementList(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        vendor_id = self.kwargs.get('pk')
        return Advertisement.objects.prefetch_related('ad_images').filter(is_active=True, user=vendor_id)

 
"""
{
    "title": "Ford Mustang 1969",
    "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
    "price": "69696",
    "currency": "USD",
    "is_auto_renew": true
}
"""
    

class NewAdImageUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdImageSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)