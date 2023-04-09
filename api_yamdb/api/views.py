from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from users.models import User
from titles.models import Title, Genre, Category
from reviews.models import Review
from .mixins import ModelMixinSet
from .filters import TitleFilter
from .permissions import (IsAdminOrReadOnlyPermission, OnlyAdmin,
                          IsAuthorAdminModeratorOrReadOnly)
from .serializers import (UserSerializer, SignUpSerializer,
                          JWTTokenSerializer, GetTitleSerializer,
                          TitleSerializer, GenreSerializer,
                          CategorySerializer, ReviewSerializer,
                          CommentSerializer, ResponseSerializer)
from .utils import generate_confirmation_code_and_send_email


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet произведения."""
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by(
        'category', 'genre', 'name', 'year'
    )
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnlyPermission,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
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


@api_view(['POST'])
def signup_function(request):
    """Функция для регистрации нового пользователя"""

    data = request.data
    resp_ser = ResponseSerializer(data=data)
    resp_ser.is_valid(raise_exception=True)
    username = resp_ser.validated_data['username']
    if not User.objects.filter(username=username).exists():
        serializer = SignUpSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        generate_confirmation_code_and_send_email(
            serializer.validated_data['username'],
            serializer.validated_data['email']
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    user = get_object_or_404(User, username=username)
    serializer = SignUpSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    if serializer.validated_data['email'] == user.email:
        serializer.save()
        generate_confirmation_code_and_send_email(
            serializer.validated_data['username'],
            serializer.validated_data['email']
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        'Вы неверно указали почту!',
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
def token_function(request):
    """Функция для получения JWT-токена"""

    serializer = JWTTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User,
                             username=serializer.validated_data['username'])
    if (user.confirmation_code == serializer.validated_data['confirmation'
                                                            '_code']):
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        return Response({'token': access_token}, status=status.HTTP_200_OK)
    return Response(
        'Неверный код подтверждения!',
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения, обновления и удаления информации
    о пользователях"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (OnlyAdmin,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=username', )
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('get', 'patch'),
        url_path='me',
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetPostPatchDeleteViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')


class ReviewViewSet(GetPostPatchDeleteViewSet):
    """Вьюсет для выполнения операций с объектами модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user,
                        title=get_object_or_404(Title, pk=title_id))


class CommentViewSet(GetPostPatchDeleteViewSet):
    """Вьюсет для выполнения операций с объектами модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title=title_id, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        serializer.save(author=self.request.user,
                        review=get_object_or_404(Review, pk=review_id,
                                                 title=title_id))
