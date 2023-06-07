import sys
from library.views import UserViewSet, BookViewSet, BookViewPurchased, BookViewPublished, Login, TransactionViewSet, TransactionAuthorView, ReadingViewSet, ReadingAuthorView

from django.urls import path
sys.path.append("..")




urlpatterns = [
    # User URLs
    path('users/', UserViewSet.as_view({'post':'post','get':'get','put':'update','delete':'delete'})),
    # Book URLs
    path('books/', BookViewSet.as_view({'post':'post','get':'get','put':'update','delete':'delete'})),
    path('books/purchased/', BookViewPurchased.as_view({'get':'get'})),
    path('books/published/', BookViewPublished.as_view({'get':'get'})),

    # Login URL
    path('login/', Login.as_view({'post':'post'})),

    # Transaction URLs
    path('transactions/', TransactionViewSet.as_view({'post':'post','get':'get'})),
    path('transactions/author/', TransactionAuthorView.as_view({'get':'get'})),

    # Reading URLs
    path('readings/', ReadingViewSet.as_view({'post':'post','get':'get','put':'update'})),
    path('readings/author/', ReadingAuthorView.as_view({'get':'get'}))
]