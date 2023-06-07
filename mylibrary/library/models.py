from django.db import models




# Register your models here.



class User(models.Model):

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    bank_account = models.CharField(max_length=50, null=True)
    upi_id = models.CharField(max_length=50, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()


    class Meta:
        db_table = 'user'
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        app_label='library'


class Book(models.Model):

    title = models.CharField(max_length=255)
    author = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    price = models.DecimalField( max_digits=6, decimal_places=2)
    royalty = models.DecimalField( max_digits=5, decimal_places=2,null=True)
    file_path = models.CharField( max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()


    class Meta:
        db_table = 'book'
        managed = True
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        app_label='library'



class Reading(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book= models.ForeignKey(Book, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    objects = models.Manager()


    class Meta:
        db_table = 'reading'
        managed = True
        verbose_name = 'Reading'
        verbose_name_plural = 'Reading'
        unique_together =('user_id','book_id')
        app_label='library'



class Transaction(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.DecimalField( max_digits=6, decimal_places=2)
    time = models.TimeField( auto_now=True)
    objects = models.Manager()



    class Meta:
        db_table = 'transaction'
        managed = True
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        unique_together =('user_id','book_id')
        app_label='library'




class User_token(models.Model):

    token = models.CharField( max_length=255,unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expiration_time = models.TimeField(auto_now=False)
    objects = models.Manager()


    class Meta:
        db_table = 'user_token'
        managed = True
        verbose_name = 'User_Token'
        verbose_name_plural = 'User_Tokens'
        app_label='library'

