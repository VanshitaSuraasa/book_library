from django.db import IntegrityError, DataError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

from ..models import Book, Transaction, Reading

from ..serializer import BookSerializer, BookSerializerPurchased, BookSerializerUnauth



def insert_book(*, request):
    """
    Inserts name, author_id, price, royalty and path of book.
    Returns false if unsuccesssful
    """
    name = request.data.get('name')
    path = request.data.get('path')
    price = request.data.get('price')
    royalty = request.data.get('royalty')


    if royalty:
        author = request.user
        print(author)
    else :
        author = None

    error = ''
    status = True


    if not name or not path or not price:
        status = False
        error += 'Name, path and price are required'


    type_dict = {name: str, path: str, price: float}
    if request.user.is_admin is True:
        author=None
        royalty=None

    elif royalty:
        type_dict[royalty] = float


    for key,value in type_dict.items():
        if not isinstance(key, value):
            error += f"- Required data type for {key} is {value}\n"


    if status is False:
        return Response(status=400, data={ "message":error})


    try:
        Book.objects.create(title=name, file_path=path,price=price,author=author,royalty=royalty)
        return Response(data=None,status=204)

    except IntegrityError as err:
        return Response(data={"message":str(err)}, status=400)

    except DataError as err:
        return Response(data={"message":str(err)}, status=400)



def retrieve_book(*,request):
    """
    Retrieves book details according to book id
    """
    
    user = request.user
    book_id= request.GET.get('book_id')
    print(user)
    data =[]

    if book_id:
        try:
            book_id = int(book_id)
    
        except ValueError:
            return Response(data={"message":"Invalid datatype of book_id"}, status= 400)

        try:
            book=Book.objects.get(id=book_id)



        except ObjectDoesNotExist:
            return Response(data={"message":"Book not found"}, status=404)


    if not user:
        
        if book_id:
            if not book.is_active:
                return Response(data={"message":"Book not found"}, status=404)
            serializer = BookSerializerUnauth(book)
            
        else:
            books = Book.objects.filter(is_active=True)
            serializer = BookSerializerUnauth(books, many=True)
            
    

    elif user.is_admin is True:
        if book_id:
            book=Book.objects.get(book_id)
            serializer = BookSerializer(book)
           

        else:
            books = Book.objects.filter()
            serializer = BookSerializer(books, many=True)
            

    else:
        if book_id:
            try:
                transactions = Transaction.objects.filter(user=user, book=book)
                book = Book.objects.get(book_id)
                serializer = BookSerializerPurchased(book)

            except ObjectDoesNotExist:
                book = Book.objects.get(id=book_id,is_active=True)
                serializer = BookSerializerUnauth(book)

        else:
            books = Book.objects.all()
            transactions = Transaction.objects.filter(user=user)
            transac_id=[]
            for transaction in transactions:
                transac_id.append(transaction.book)

            for book in books:
                if book in transac_id:
                    serializer = BookSerializerPurchased(book)
                    data.append(serializer.data)
                    print(data)
                
                elif user == book.author:
                    serializer = BookSerializer(book)
                    data.append(serializer.data)
                    print(data)


                else:
                    if book.is_active:
                        serializer = BookSerializerUnauth(book)
                        data.append(serializer.data)

                        print(type(data))

    if not data:
        data = serializer.data

    return Response(data=data, status=200, content_type="application/json")





def retrieve_book_by_author(*,request):
    """
    Retrieves book details according to author
    """
    
    user = request.user
    book_id= request.GET.get('book_id')
    data =[]

    if not user:
        return Response(data={"message":"Unauthorized"}, status= 401)

    if book_id:
        try:
            book_id = int(book_id)
        
        except ValueError:
            return Response(data={"message":"Invalid datatype of book_id"}, status= 400)
            

    if book_id:
        try:
            book = Book.objects.get(id=book_id)

            if not book.author_id == user.id:
                return Response(data={"message":"Unauthorized"}, status= 401)

            serializer = BookSerializerPurchased(book)

        except ObjectDoesNotExist:
            return Response(data={"message":"No matching record found"}, status=404)

    else:
        books = Book.objects.filter(author_id=user.id)
        serializer = BookSerializer(books, many= True)
        data = serializer.data
    return Response(data=data, status=200, content_type="application/json")




def retrieve_purchased(*,request):
    """
    Retrieves books that are purchased but not being read.
    """

    user = request.user
    book_id= request.GET.get('book_id')
    data =[]

    if not user:
        return Response(data={"message":"Unauthorized"}, status= 401)

    if book_id:
        try:
            book_id = int(book_id)

        except ValueError:
            return Response(data={"message":"Invalid datatype of book_id"}, status= 400)

    try:
        transactions = Transaction.objects.filter(user=user)
        transac_id=[]
        for transaction in transactions:
            transac_id.append(transaction.book)
        
        print(transac_id)

    except ObjectDoesNotExist:
        return Response(data={"message":"No books purchased found"}, status= 404)

    readings = Reading.objects.filter(user=user)
    read_id=[]
    for reading in readings:
        read_id.append(reading.book)

    if book_id:
        try:
            book = Book.objects.get(id=book_id)

            if not book in transac_id:
                return Response(data={"message":"Book not purchased"}, status= 404)

            if book in read_id:
                return Response(data={"message":"Book started reading"}, status= 404)

            serializer = BookSerializerPurchased(book)
            data = serializer.data

        except ObjectDoesNotExist:
            return Response(data={"message":"No matching record found"}, status=404)

    else:
        for book in transac_id:
            if book not in read_id:
                try:
                    serializer = BookSerializerPurchased(book)
                    data.append(serializer.data)
                except ObjectDoesNotExist:
                    return Response(data={"message":"No matching record found"}, status=404)


    return Response(data=data, status=200, content_type="application/json")


def update_book(*,request):
    """
    Update royalty to author by user input
    """

    user=request.user
    if not user:
        return Response(data={'message':"Unauthorized"},status=401)

    error =''
    status = True
    
    book_id = request.data.get("book_id")
    if not book_id:
        error += "Book_id is required"

    if not isinstance(book_id,int):
        error+= "Book_id should be int"

    price = request.data.get("price")
    royalty = request.data.get('royalty')

    if user.is_admin:
        if not price and not royalty:
            error += "Royalty or price is required"
            status=False

    else:
        if not price:
            error += "Price is required"
            status = False

    
    if price:
        if not isinstance(price, float):
            error += "Price should be float"
            status = False


    if royalty:
        if not isinstance(royalty, float):
            error += "Royalty should be float"
            status = False


    if status is False:
        return Response(data={"message":error }, status = 400)

    if user.is_admin:
        try:
            book = Book.objects.get(id=book_id)

            if price:
                book.price = price

            if royalty:
                book.royalty = royalty
            
            book.save()

        except ObjectDoesNotExist:
            return Response(data={"message":"Book does not exist"},status=404)

    else:
        try:
            book = Book.objects.get(id=book_id)
        
            if price and book.author==user:
                book.price = price

            book.save()
        
        except ObjectDoesNotExist:
            return Response(data={"message":"Book does not exist"},status=404)

    return Response(data=None, status=204)





def delete_book(*,request):
    """
    Deacivate book by book id
    """
    
    
    user=request.user
    if not user:
        return Response(data={'message':"Unauthorized"},status=401)

    error =''
    status = True
    book_id = request.data.get("book_id")
    if not book_id:
        error += "Book_id is required"

    if not isinstance(book_id,int):
        error+= "Book_id should be int"
    
    if status is False:
        return Response(data={"message":error}, status =400)
    
    book = Book.objects.get(id=book_id)

    
    try:
        book = Book.objects.get(id=book_id)
    
        if user.is_admin is True or book.author==user:
            book.is_active = False
            book.save()

    except ObjectDoesNotExist:
        return Response(data={"message":"Book does not exist"},status=404)
    
    return Response(data=None, status=204)
