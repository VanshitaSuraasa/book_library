# Create your views here.
from rest_framework.viewsets import ViewSet
from .helpers.user import insert_user,retrieve_user,update_password,delete_user
from .helpers.book import insert_book,retrieve_book,retrieve_book_by_author,retrieve_purchased,update_book,delete_book
from .helpers.transactions import insert_transaction,retrieve_transaction,retrieve_transaction_by_author
from .helpers.reading import insert_reading,retrieve_reading,retrieve_reading_by_author,book_completed
from .helpers.tokens import insert_token,validate_token
from .models import User
from rest_framework.response import Response


# Create your views here.

class UserViewSet(ViewSet):

    def post(self,request):
        return insert_user(request=request)

    def get(self,request):
        user = validate_token(request=request)
        if not isinstance(user, User):
            return Response(data={"message":"Unauthorized"}, status=401)
        request.user=user
        return retrieve_user(request=request)

    def update(self,request):
        user = validate_token(request=request)
        if not isinstance(user, User):
            return Response(data={"message":"Unauthorized"}, status=401)
        request.user=user
        return update_password(request=request)
    
    def delete(self,request):
        user = validate_token(request=request)
        if not isinstance(user, User):
            return Response(data={"message":"Unauthorized"}, status=401)
        request.user=user
        return delete_user(request=request)

class BookViewSet(ViewSet):

    def post(self,request):
        user = validate_token(request=request)
        if not isinstance(user, User):
            return Response(data={"message":"Unauthorized"}, status=401)
        request.user=user
        return insert_book(request=request)

    def get(self,request):
        user = validate_token(request=request)
        if not isinstance(user, User):
            user=None
        request.user=user
        return retrieve_book(request=request)

    def update(self,request):
        user = validate_token(request=request)
        if not isinstance(user, User):
            return Response(data={"message":"Unauthorized"}, status=401)
        request.user=user
        return update_book(request=request)
        
    def delete(self,request):
        user = validate_token(request=request)
        if not isinstance(user, User):
            return Response(data={"message":"Unauthorized"}, status=401)
        request.user=user
        return delete_book(request=request)

class BookViewPurchased(ViewSet):

    def get(self,request):
        user = validate_token(request=request)
        if not isinstance(user, User):
            return Response(data={"message":"Unauthorized"}, status=401)
        request.user=user
        return retrieve_purchased(request=request)

class BookViewPublished(ViewSet):

    def get(self,request):
        user = validate_token(request=request)
        if not isinstance(user, User):
            return Response(data={"message":"Unauthorized"}, status=401)
        request.user=user
        return retrieve_book_by_author(request=request)

class Login(ViewSet):
    def post(self,request):
        return insert_token(request=request)

class TransactionViewSet(ViewSet):
    def post(self,request):
        user = validate_token(request=request)
        if not isinstance(user, User):
            return Response(data={"message":"Unauthorized"}, status=401)
        request.user=user
        return insert_transaction(request=request)

    def get(self,request):
        user = validate_token(request=request)
        if not isinstance(user, User):
            return Response(data={"message":"Unauthorized"}, status=401)
        request.user=user
        return retrieve_transaction(request=request)

class TransactionAuthorView(ViewSet):
    def get(self,request):
        user = validate_token(request=request)
        if not isinstance(user, User):
            return Response(data={"message":"Unauthorized"}, status=401)
        request.user=user
        return retrieve_transaction_by_author(request=request)

class ReadingViewSet(ViewSet):
    def post(self,request):
        user = validate_token(request=request)
        if not isinstance(user, User):
            return Response(data={"message":"Unauthorized"}, status=401)
        request.user=user
        return insert_reading(request=request)

    def get(self,request):
        user = validate_token(request=request)
        if not isinstance(user, User):
            return Response(data={"message":"Unauthorized"}, status=401)
        request.user=user
        return retrieve_reading(request=request)

    def update(self,request):
        user = validate_token(request=request)
        if not isinstance(user, User):
            return Response(data={"message":"Unauthorized"}, status=401)
        request.user=user
        return book_completed(request=request)

class ReadingAuthorView(ViewSet):
    def get(self,request):
        user = validate_token(request=request)
        if not isinstance(user, User):
            return Response(data={"message":"Unauthorized"}, status=401)
        request.user=user
        return retrieve_reading_by_author(request=request)








    
