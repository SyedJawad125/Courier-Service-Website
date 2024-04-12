from django.urls import path
from user_auth.views import *

urlpatterns = [
    path('register', RegisterAPIView.as_view({"post": "create"}), name='register'),
    path('login', LoginAPIView.as_view({"post": "login"}), name='login'),
    path('logout', LogoutAPIView.as_view({"post": "logout"}), name='logout'),
    path('change-password', ChangePasswordAPIView.as_view({"post": "post"}), name='change_password'),
    path('listing', UserListingAPIView.as_view({"get":"get_user"}), name='listing'),

    # 'listing'   
]