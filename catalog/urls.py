from django.urls import path, re_path
from . import views



app_name = 'catalog'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),           
    path('index/', views.index, name='index'),     
    path('author/', views.author, name='author'),  
    path('books_list/', views.books_list, name='books_list'),  
    path('genre_list/', views.genre_list, name='genre_list'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name="book_detail"),
    re_path(r'^book/(?P<pk>\d+)$', views.BookListView.as_view(), name='books'),
    # re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('my-view', views.MyView.as_view(), name='my-view'),
    re_path(r'^book/(?P<pk>[-\w]+)/renew/$',
            views.renew_book_librarian,
            name= 'renewal-book-librarian'),
    re_path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('all-borrowed/', views.AllBorrowedBooksListView.as_view(), name='all-borrowed'),
]
# urlpatterns += [
#     re_path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
# ]


# urlpatterns += [
#     path('books/year/<int:year>/', views.books_list_year, name='books_list_year'),
#     path('books/year/<int:year>/month/<int:month>', views.books_list_month, name='books_list_month'),
#     path('books/year/<int>:year>month/<int:month/day/<int:day>/', views.views.books_list_day, name='books_list_day'),
# ]

# urlpatterns += [
#     re_path(r'^books/(?P<year>[0-9]{4})/$', views.book_list_year, name='books_list_year'),
#     re_path(r'^books/(?P<year>[0-9]{4}/)/(?P<month>0?[1-9]|1[0:2])/$', views.views.books_list_month, name='books_list_month'),
#     re_path(r'^books/(?P<year>[0-9]{4}/)/(?P<month>0?[1-9]|1[0:2])/(?P<day>0?[])/$')
# ]