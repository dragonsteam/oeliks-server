# from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import User, Advertisement
from .serializers import UserSerializer, AdvertisementSerializer


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


@api_view(["GET"])
@permission_classes([AllowAny])
def ping_pong(request):
    # update_trucks()
    return Response("pong", status=status.HTTP_200_OK)

#
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)

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


@api_view(["GET"])
@permission_classes([AllowAny])
def users(request):
    pass


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def advertisements(request):
    if request.method == "GET":
        ads = Advertisement.objects.filter(is_active=True)
        serializer = AdvertisementSerializer(ads, many=True)
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
    "about": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
    "price": "69696",
    "currency": "USD",
    "is_auto_renew": true
}
"""