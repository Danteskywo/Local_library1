from django.urls import path, re_path
from catalog import views


app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('author/', views.author, name='author'),
    # path('books/', views.books, name='books'),

]


urlpatterns = [
    # path('', views.BookListView.as_view(), name = 'index'),
    # path('books/', views.BooklistView.as_view(), name = 'book-list'),
    # path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    # path('authors/', views.AuthorListView.as_view(), name='author-list'),
    # path('author/<int:pk>/', views.AuthorDetailView.as_view(),
    #      name='author-detail'),
    # path('create/', views.CreateBookView.as_view(),
    #      name='create-book'),
    # path('edit/<int:pk>/', views.EditBookView.as_view(),
    #      name='create-book'),
    # path('delete/<int:pk>/', views.EditBookView.as_view(),
    #      name='create-book'),
         
]
