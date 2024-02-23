# from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import User
from .serializers import UserSerializer


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