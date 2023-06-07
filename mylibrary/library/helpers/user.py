"""
Contain all the operations concerning the user. Operations such as
insert, update, delete, retrieve.
"""
from django.core.exceptions import ObjectDoesNotExist , ValidationError
from django.db import IntegrityError
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response

from ..serializer import UserSerializer

from ..models import User


def is_valid_email(email):

    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def insert_user(*,request):
    """
    This function takes name, email, password, account number, upi id
    as input and adds it to user table. Returns true if operation was successful
    and false with error if unsuccessful.
    """
    error= ''
    status = True
    print(request.POST)
    name = request.data.get("name")
    email = request.data.get('email')
    account_num = request.data.get('account_number')
    upi_id= request.data.get('upi_id')
    password = request.data.get('password')


    if not name or not email or not password:
        error += "Name, email, and password are required"
        status = False

    fields = [name,email,password]
    if account_num:
        fields.append(account_num)

    if upi_id:
        fields.append(upi_id)

    for key in fields:
        if not isinstance(key, str):
            error += f"- Required data type for {key} is str\n"
            status= False

    if not is_valid_email(email):
        status=False
        error += "Invalid Email"

    if status is False:
        return Response(status=400, data={ "message":error})

    
    hashed_password = make_password(password)


    try:
        User.objects.create(name=name,email=email,password=hashed_password,
        upi_id=upi_id,bank_account=account_num)
        return Response(data=None,status=204)

    except IntegrityError as err:
        error = str(err)
        return Response(status=400, data={ "message":error})

    except ValidationError as err:
        error = str(err)
        return Response(status=400, data={ "message":error})




def retrieve_user(*, request):
    """
    This function takes user_id .
    """

    if request.user.is_admin is True:

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=200, content_type="application/json")

    else:
        try:
            user = User.objects.get(id=request.user.id)
            serializer = UserSerializer(user)
            return Response(data=serializer.data, status=200, content_type="application/json")

    
        except ObjectDoesNotExist:
            return Response(data={"message":"User not found"}, status=404)



def authenticate(*, request):
    """
    Authenticates user email by checking password entered
    """
    email = request.data.get('email')
    password = request.data.get('password')

    status= True
    error = ''
    if  not email or not password:
        error += "Email, and password are required\n"
        status = False

    fields=[email,password]

    for key in fields:
        if not isinstance(key, str):
            error += f"- Required data type for {key} is str\n"
            status= False

    if not is_valid_email(email):
        status=False
        error += "Invalid Email"

    if status is False:
        return Response(data={"message":error}, status=400)

    try:
        user = User.objects.get(email=email,is_active=True)

        if check_password(password, user.password):
            return True
        else:
            return Response(data={"message":"Invalid Password"},status=401)

    except ObjectDoesNotExist:
        return Response(data={"message":"User not found"}, status=404)

    except ValidationError as err:
        error = str(err)
        return Response(status=400, data={ "message":error})




def update_password(*, request):
    """
    Autheticates user email with current password, and updates password with new password
    """

    email = request.data.get('email')
    password = request.data.get('password')
    new_password = request.data.get('new_password')

    status= True
    error = ''
    if  not email or not password or not new_password:
        error += "Email, password and new_password are required\n"
        status = False

    fields=[email,password,new_password]

    for key in fields:
        if not isinstance(key, str):
            error += f"- Required data type for {key} is str\n"
            status= False

    if not is_valid_email(email):
        status=False
        error += "Invalid Email"

    if status is False:
        return Response(data={"message":error}, status=400)


    auth = authenticate(request=request)
    if auth is not True:
        return auth

    try:
        user = User.objects.get(email=email)
        hashed_password = make_password(new_password)
        user.password=hashed_password
        user.save()
        return Response(data=None, status=204)


    except ObjectDoesNotExist:
        return Response(data={"message":"User not found"}, status=404)
    
    except ValidationError as err:
        error = str(err)
        return Response(status=400, data={ "message":error})



def delete_user(*, request):
    """
    Authenticates user email and inactivates if authenticated
    """
    user_id = request.data.get('user_id')
    user=request.user
    if not user.is_admin:
        return Response(data={"message":"Unauthroized"},status=401)
    
    status= True
    error = ''
    if  not user_id:
        error += "User_id required"
        status = False

    if not isinstance(user_id, int):
        error += " Required data type for user_id is int\n"
        status= False

    
    if status is False:
        return Response(data={"message":error}, status=400)

    try:
        user = User.objects.get(id=user_id)
        user.is_active=False
        user.save()
        return Response(data=None, status=204)


    except ObjectDoesNotExist:
        return Response(data={"message":"User not found"}, status=404)
