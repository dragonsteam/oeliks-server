# from django.core.cache import cache
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language, activate, gettext
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Advertisement, AdImage, Section
from .serializers import UserSerializer, TelegramUserSerializer, AdvertisementSerializer, AdvertisementsSerializer, AdImageSerializer, SectionSerializer

from core.utility import log

def custom404(request, exception=None):
    return JsonResponse(
        {"status_code": 404, "detail": "The resourse was not found"}, status=404
    )


# def check_access(user, source: str, type):
#     # if superuser always pass him :)
#     if user.is_superuser:
#         return True

#     access = Access.objects.filter(pk=user.access_id).values(source)
#     # print(str(access.query))
#     if access:
#         return type in access[0][source]
#     return False

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
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)

    # return Response(
    #     {'detail': _('regular registration has been disabled by developers, please use Telegram to proceed')},
    #     status=status.HTTP_400_BAD_REQUEST,
    # )

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"success": "user has been succesfully created"},
            status=status.HTTP_201_CREATED,
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
    )

"""
{
    "first_name": "John",
    "last_name": "Doe",
    "phone": "901558090",
    "password": "1234"
}
"""

@api_view(["POST"])
@permission_classes([AllowAny])
def telegram_auth(request):
    serializer = TelegramUserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refreshToken": str(refresh),
                "accessToken": str(refresh.access_token)
            },
            status=status.HTTP_200_OK,
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST,
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


@api_view(["GET"])
@permission_classes([AllowAny])
def users(request):
    pass


@api_view(["GET"])
@permission_classes([AllowAny])
def sections(request):
    sections = Section.objects.prefetch_related('section_category').all()
    serializer = SectionSerializer(sections, many=True)
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([AllowAny]) ###
def advertisements(request):
    if request.method == "GET":
        ads = Advertisement.objects.prefetch_related('ad_images').filter(is_active=True)
        serializer = AdvertisementsSerializer(ads, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    if request.method == "POST":
        serializer = AdvertisementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": "advertisement has been succesfully created"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
 
"""
{
    "title": "Ford Mustang 1969",
    "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
    "price": "69696",
    "currency": "USD",
    "is_auto_renew": true
}
"""

@api_view(["GET"])
@permission_classes([AllowAny])
def advertisement(request, id):
    ads = Advertisement.objects.prefetch_related('ad_images').get(pk=id)
    serializer = AdvertisementSerializer(ads)
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def vip_ads(request):
    ads = Advertisement.objects.prefetch_related('ad_images').filter(is_active=True)
    serializer = AdvertisementSerializer(ads, many=True)
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def ad_images(request, id):
#     if request.method == "GET":
#         ads = AdImage.objects.all()
#         serializer = AdImageSerializer(ads, many=True)
#         return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    

class NewAdImageUploadAPIView(APIView):
    # parser_classes = (MultiPartParser, FormParser)
    serializer_class = AdImageSerializer
    # permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # you can access the file like this from serializer
            # uploaded_file = serializer.validated_data["file"]
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )