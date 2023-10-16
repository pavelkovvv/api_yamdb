from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenresViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, signup_function,
                    token_function)

router_v1 = routers.DefaultRouter()
router_v1.register(r'genres', GenresViewSet, basename='genres')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(
    r'titles', TitleViewSet,
    basename='title')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='review')

app_name = 'api'

urlpatterns = [
    path('v1/auth/signup/', signup_function, name='signup'),
    path('v1/auth/token/', token_function, name='token'),
    path('v1/', include(router_v1.urls))
]
