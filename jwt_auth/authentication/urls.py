from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenObtainSlidingView,

    TokenRefreshSlidingView,
    TokenRefreshView,
)

from .views import CustomObtainTokenPairWithPhoneView, CustomUserCreateView, LogoutAndBlacklistRefreshTokenForUserView

urlpatterns = [
    path('token/obtain/pair/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # refresh & access token
    path('token/custom/obtain/pair/', CustomObtainTokenPairWithPhoneView.as_view(), name='token_custom_obtain_pair'),  # refresh & access token
    path('token/obtain/sliding/', TokenObtainSlidingView.as_view(), name='token_obtain_sliding'),  # token



    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/refresh/sliding/', TokenRefreshSlidingView.as_view(), name='token_refresh_sliding'),

    path('user/create/', CustomUserCreateView.as_view(), name="create_user"),
    path('blacklist/', LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='blacklist'),
]