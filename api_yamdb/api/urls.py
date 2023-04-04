from rest_framework import routers

from django.urls import path, include

from .views import (signup_function, token_function,
                    UserViewSet, ReviewViewSet,
                    CommentViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')

app_name = 'api'

urlpatterns = [
    path('v1/auth/signup/', signup_function, name='signup'),
    path('v1/auth/token/', token_function, name='token'),
    path('v1/', include(router_v1.urls))
]
