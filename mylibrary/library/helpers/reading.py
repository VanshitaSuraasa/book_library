"""
Contain all the operations concerning the reading module. Operations such as
insert, update, delete, retrieve.
"""
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

from ..models import Book,Reading,Transaction

from ..serializer import ReadingSerializer

def insert_reading(*,request):
    """
    This function takes user id, and book id and inserts it in the reading table.
    Returns true if operation was successful and false with error if unsuccessful.
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

    except ObjectDoesNotExist:
        return Response(data={"message":"Book not found"},status =404)

    if not book.author_id == request.user.id:
        try:
            Transaction.objects.get(book=book,user=request.user)

        except ObjectDoesNotExist:
            return Response(data={"message":"Book not purchased"},status =400)

    try:
        reading = Reading.objects.get(user=request.user,book=book)
        serializer = ReadingSerializer(reading)
        return Response(status=200, data=serializer.data, content_type="application/json")

    except ObjectDoesNotExist:
        try:
            Reading.objects.create(book=book,user=request.user)
            return Response(status=204,data=None)


        except IntegrityError as err:
            return Response(data={"message":str(err)}, status=400)


def retrieve_reading(*, request):
    """
    This function takes user_id, book_id or both and retrieves matching columns from reading table.
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
            reading = Reading.objects.filter(user=user, book=book)
            serializer = ReadingSerializer(reading)

        except ObjectDoesNotExist:
            return Response(data={"message":"No matching record found"}, status=404)

    else:
        readings = Reading.objects.filter(user=user)
        serializer = ReadingSerializer(readings,many=True)

    return Response(data=serializer.data, status=200, content_type="application/json")



def retrieve_reading_by_author(*, request):
    """
    This function takes user_id and retrieves books published by an author.
    """
    if not request.user.id:
        return Response(data={"message":"Unauthorized"},status=401)

    book_id= request.GET.get('book_id')
    data =[]

    if book_id:
        try:
            book_id = int(book_id)
    
        except ValueError:
            return Response(data={"message":"Invalid datatype of book_id"}, status= 400)

        try:
            book=Book.objects.get(id=book_id)
            
        except ObjectDoesNotExist:
            return Response(data={"message":"Book does not exist"}, status= 404)


    if book_id:
        if request.user==book.author:
            try:
                readings = Reading.objects.filter(book=book)
                serializer = ReadingSerializer(readings,many=True)
                data.append(serializer.data)

            except ObjectDoesNotExist:
                return Response(data={"message":"No matching record found"}, status=404)
        
        else:
            return Response(data={"message":"Unauthroized"},status=401)

    else:
        books=Book.objects.filter(author=request.user)
        for book in books:
            readings = Reading.objects.filter(book=book)
            serializer = ReadingSerializer(readings,many=True)
            data.append(serializer.data)

    
    return Response(data=data, status=200, content_type="application/json")


def book_completed(*, request):
    """
    This function updates a book to be completed with regards to a user.
    Returns true if operation was successful and false with error if unsuccessful.
    """
    if not request.user.id:
        return Response(data={"message":"Unauthorized"},status=401)

    book_id= request.GET.get('book_id')

    if not book_id:
        return Response(data={"message":"Book_id required"},status=400)
        
    try:
        book_id = int(book_id)

    except ValueError:
        return Response(data={"message":"Invalid datatype of book_id"}, status= 400)

    try:
        book=Book.objects.get(id=book_id)
        
    except ObjectDoesNotExist:
        return Response(data={"message":"Book does not exist"}, status= 404)

    
    try:
        reading = Reading.objects.get(book_id=book,user_id= request.user)
        reading.is_completed = True
        reading.save()
        return Response(data=None, status=204)

        
    except ObjectDoesNotExist:
        return Response(data={"message":"No matching record found"}, status=404)
    

