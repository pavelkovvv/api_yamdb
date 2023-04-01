from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from .serializers import (UserSerializer, SignUpSerializer, JWTTokenSerializer)
from users.models import User
from .utils import (get_object_or_none,
                    generate_confirmation_code_and_send_email)


@api_view(['POST'])
def signup_function(request):
    """Функция для регистрации нового пользователя"""

    data = request.data
    username = data.get('username')
    if not User.objects.filter(username=username).exists():
        serializer = SignUpSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        if data['username'] == 'me':
            raise ValidationError("В качестве 'username' нельзя"
                                  " использовать 'me'!")
        serializer.save()
        generate_confirmation_code_and_send_email(data['username'],
                                                  data['email'])
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        user = get_object_or_404(User, username=username)
        serializer = SignUpSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['email'] == user.email:
            serializer.save()
            generate_confirmation_code_and_send_email(data['username'],
                                                      data['email'])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            'Вы неверно указали почту!',
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def token_function(request):
    """Функция для получения JWT-токена"""

    data = request.data
    serializer = JWTTokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, username=data['username'])
        if user.confirmation_code == data['confirmation_code']:
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)
            return Response({'token': access_token}, status=status.HTTP_200_OK)
        return Response(
            'Неверный код подтверждения!',
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
