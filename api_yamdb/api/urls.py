from rest_framework import routers

from django.urls import path, include

from .views import (signup_function, token_function)


router = routers.DefaultRouter()

app_name = 'api'

urlpatterns = [
    path('v1/auth/signup/', signup_function, name='signup'),
    path('v1/auth/token/', token_function, name='token'),
    path('v1/', include(router.urls))
]
