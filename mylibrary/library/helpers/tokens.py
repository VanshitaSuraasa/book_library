"""
Contains operations regarding token model
"""


import uuid
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response



from ..models import User,User_token
from .user import authenticate


def insert_token(*, request):
    """
    Inserts token in user_token table with row user_id.
    """

    auth = authenticate(request=request)
    if auth is not True:
        return auth

    token = str(uuid.uuid4())
    expiration_time= datetime.now() + timedelta(seconds=3600)
    user = User.objects.get(email=request.data.get('email'))

    try:
        user_token = User_token.objects.get(user=user)
        user_token.token=token
        user_token.expiration_time = expiration_time
        user_token.save()

    except ObjectDoesNotExist:
        User_token.objects.create(user=user, token=token, expiration_time=expiration_time)

    return Response(data={"token":token},status=200,content_type="application/json")





def validate_token(*, request):
    """
    Validates token and returns if user is admin
    """
    token= request.headers.get("Authorization")
    status=True

    error=''
    

    if not token:
        error+=  "Token is required"
        status = False

    if not isinstance(token , str):
        error = "Token should be str"
        status = False

    if not token.startswith("Bearer"):
        error= "Invalid Token"
        status = False

    try:
        token=token.split(' ')[1]

    except IndexError:
        error= "Invalid Token"
        status = False

    if status is False:
        return Response(data={"message":error},status=400)

     
    current_time = datetime.now().time()


    try:
        user_token= User_token.objects.get(token=token)

    except ObjectDoesNotExist:
        return None
    
    if user_token.expiration_time<current_time:
        return None

    user=User.objects.get(id=user_token.user_id)
    return user

