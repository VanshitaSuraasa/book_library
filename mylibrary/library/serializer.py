from rest_framework import serializers
from .models import User,User_token,Book,Reading,Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email','bank_account','upi_id']


class BookSerializer(serializers.ModelSerializer):
    id= serializers.ReadOnlyField()
    class Meta:
        model=Book
        fields =['id','title','file_path','price','author','royalty']

class BookSerializerPurchased(serializers.ModelSerializer):
    id=serializers.ReadOnlyField()
    class Meta:
        model=Book
        fields =['id','title','file_path','price','author']

class BookSerializerUnauth(serializers.ModelSerializer):
    id=serializers.ReadOnlyField()
    class Meta:
        model=Book
        fields =['id','title','price','author']

class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reading
        fields =['user','book','is_completed']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields = ['user','book','amount','time']

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model=User_token
        fields = ["__all__"]