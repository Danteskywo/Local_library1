from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre



# Create your views here.
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books=Book.objects.all().count()

    num_instances=BookInstance.objects.all().count()
    
    # Доступные книги (статус = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    
    num_authors=Author.objects.count()
      # Метод 'all()' применён по умолчанию
    num_genre = Genre.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1


    return render(
        request,'index.html',
        context={'num_books':num_books,
                 'num_instances':num_instances,
                 'num_instances_available':num_instances_available,
                 'num_authors':num_authors,
                 'num_genre':num_genre,
                 'num_visits':num_visits
                 }
                 )







def author(request):
    author_list=list(Author.objects.all())
    return render(
        request, "author.html",
          context={'author_list':author_list})

# def book_search(request):
#     return render(request, "catalog/book_search", context={
#         'books':books,
#         'query':query,
#         'results_count':book_search
#     })


def books(request):
    books_all = Book.objects.all()
    books_all = list(books_all)
    books_str = ', '.join([book.title for book in books_all])
    num_visits_book = request.session.get('num_visits_book', 0)
    request.session['num_visits_book'] = num_visits_book+1
    return render(
        request, "books.html",
          context={'num_visits_book':num_visits_book,
                   'books_all':books_str,
                   
                   })


