"""
Contain all the operations concerning the transaction module. Operations such as
insert, update, delete, retrieve.
"""

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

from ..models import Book, Transaction

from ..serializer import TransactionSerializer

def insert_transaction(*, request):
    """
    This function takes book_id, user_id, amount
    as input and adds it to user table.
    """
    if not request.user.id:
        return Response(data={"message":"Unauthorized"},status=401)


    book_id = request.data.get('book_id')


    error = ''
    status = True


    if not book_id:
        status = False
        error += 'Book_id is required'

    if not isinstance(book_id, int):
        error += "Required data type for book_id is int\n"


    if status is False:
        return Response(status=400, data={ "message":error})


    try:
        book=Book.objects.get(id=book_id)
        if not book.is_active:
            return Response(data={"message":"Book cannot be purchased"},status =404)


    except ObjectDoesNotExist:
        return Response(data={"message":"Book not found"},status =404)

    amount = book.price

    if book.author== request.user:
        return Response(data={"message":"Author cannot purchase their own book"}, status=400)

    try:
        Transaction.objects.create(book=book,user=request.user,amount=amount)

    except IntegrityError as err:
        return Response(data={"message":str(err)}, status=400)

    return Response(status=204,data=None)



def retrieve_transaction(*, request):
    """
    Retrieves transaction details according to user_id
    """
    user = request.user

    if not request.user.id:
        return Response(data={"message":"Unauthorized"},status=401)

    book_id= request.GET.get('book_id')

    if book_id:
        try:
            book_id = int(book_id)
            book=Book.objects.get(book_id)
    
        except ValueError:
            return Response(data={"message":"Invalid datatype of book_id"}, status= 400)


    if book_id:
        try:
            transaction = Transaction.objects.filter(user=user, book=book)
            serializer = TransactionSerializer(transaction)

        except ObjectDoesNotExist:
            return Response(data={"message":"No matching record found"}, status=404)

    else:
        transactions = Transaction.objects.filter(user=user)
        serializer = TransactionSerializer(transactions,many=True)

    return Response(data=serializer.data, status=200, content_type="application/json")
    


def retrieve_transaction_by_author(*, request):
    """
    Retrieves transaction details according to author
    """
    
    if not request.user:
        return Response(data={"message":"Unauthorized"},status=401)

    book_id= request.GET.get('book_id')
    data =[]

    if book_id:
        try:
            book_id = int(book_id)
            book=Book.objects.get(book_id)
    
        except ValueError:
            return Response(data={"message":"Invalid datatype of book_id"}, status= 400)

        try:
            book=Book.objects.get(id=book_id)
            
        except ObjectDoesNotExist:
            return Response(data={"message":"Book does not exist"}, status= 404)


    if book_id:
        if request.user==book.author:
            try:
                transactions = Transaction.objects.filter(book=book)
                serializer = TransactionSerializer(transactions,many=True)
                data=serializer.data

            except ObjectDoesNotExist:
                return Response(data={"message":"No matching record found"}, status=404)
        
        else:
            return Response(data={"message":"Unauthroized"},status=401)

    else:
        books=Book.objects.filter(author=request.user)
        for book in books:
            transactions = Transaction.objects.filter(book=book)
            serializer = TransactionSerializer(transactions,many=True)
            data.append(serializer.data)


    return Response(data=serializer.data, status=200, content_type="application/json")