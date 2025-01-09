from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChangePasswordView,
    LoginApiViews,
    LogoutApiView,
    RegisterApiView,
    UserProfileUpdateView,
)
urlpatterns = [
    path('login/', LoginApiViews.as_view()),
    path('register/', RegisterApiView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('logout/', LogoutApiView.as_view(), name='logout'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
]
