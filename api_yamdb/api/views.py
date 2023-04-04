from django.db.models import Avg
from rest_framework import status, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter


from .mixins import ModelMixinSet
from .filters import TitleFilter
from .permissions import (IsAdminOrReadOnlyPermission, IsAdminUser)
from .serializers import (UserSerializer, SignUpSerializer,
                          JWTTokenSerializer, GetTitleSerializer,
                          TitleSerializer, GenreSerializer,
                          CategorySerializer)
from users.models import User
from titles.models import Title, Genre, Category
from .utils import (get_object_or_none,
                    generate_confirmation_code_and_send_email)


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet произведения."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).prefetch_related(
        'category', 'genre'
    )
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = TitleFilter
    permission_classes = (IsAdminOrReadOnlyPermission,)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleSerializer
        return GetTitleSerializer


class GenresViewSet(ModelMixinSet):
    """ViewSet жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (SearchFilter, )
    filterset_fields = ('name', 'slug')
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class CategoryViewSet(ModelMixinSet):
    """ViewSet категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (SearchFilter,)
    filterset_fields = ('name', 'slug')
    search_fields = ('name', 'slug',)
    lookup_field = 'slug'


class UserViewSet(viewsets.ModelViewsSet):
    """ViewSet User"""
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer

    @action(detail=False,
            methods=(['GET', 'PATCH']),
            permission_classes=[IsAuthenticated])
    def me(self, request):
        """Получение данных текущего зарегистрированного пользователя."""
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        serializer = UserSerializer(
            request.user, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)


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


class CommentViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    pass


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
