# Rest Framework
from rest_framework.authentication import TokenAuthentication


class AfetHaritaAuthentication(TokenAuthentication):
    keyword = "AfetHarita"
