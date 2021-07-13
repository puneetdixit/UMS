from rest_framework.authentication import TokenAuthentication
from ums.models import CustomToken

class CustomTokenModel(TokenAuthentication):
    model = CustomToken