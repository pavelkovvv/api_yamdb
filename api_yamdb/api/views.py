from rest_framework import status

from rest_framework.decorators import api_view, authentication_classes
#from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response

from .serializers import (UserSerializer, SignUpSerializer, JWTTokenSerializer)
from users.models import User


@api_view(['POST'])
def signup_function(request):
    """Функция для регистрации нового пользователя"""
    ВСЁ ПЕРЕПИСАТЬ!!!!!!!!!!
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        #print(request.data)
        print('yees')
        return Response(request.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def token_function(request):
    """Функция для получения JWT-токена"""
    pass
