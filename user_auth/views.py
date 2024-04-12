from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from utils.base_authentication import JWTAuthentication
from user_auth.user_controller import *


register_controller = RegisterController()
login_controller = LoginController()
logout_controller = LogoutController()
change_password_controller = ChangePasswordController()
user_listing_controller = UserListingController()


class RegisterAPIView(ModelViewSet):
    def create(self, request):
        return register_controller.create(request)



class LoginAPIView(ModelViewSet):
    def login(self,request):
        return login_controller.login(request)
    
class LogoutAPIView(ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    
    def logout(self,request):
        return logout_controller.logout(request)
    
class ChangePasswordAPIView(ModelViewSet):
    
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self,request):
        return change_password_controller.change_password(request)
    

class UserListingAPIView(ModelViewSet):
    
    authentication_classes = (JWTAuthentication,)
    
    def get_user(self,request):
        return user_listing_controller.get_user(request)