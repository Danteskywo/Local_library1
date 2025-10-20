from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre
from django.views import generic



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


def books_list(request):
    books_all = Book.objects.all()
    books_all = list(books_all)
    num_visits_book = request.session.get('num_visits_book', 0)
    request.session['num_visits_book'] = num_visits_book+1
    return render(
        request, "book_list.html",
          context={'num_visits_book':num_visits_book,
                   'books_all':books_all,
                   
                   })


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    queryset = Book.objects.all()
    template_name = 'book_list.html'


def genre_list(request):
    genre_all = Genre.objects.all()
    genre_all = list(genre_all)
    num_visits_genre = request.session.get('num_visits_genre', 0)
    request.session['num_visits_genre'] = num_visits_genre+1
    return render(
        request, "genre_list.html",
          context={'num_visits_genre':num_visits_genre,
                   'genre_all':genre_all,
                   
                   })

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super.get_context_data(**kwargs)

        book = self.get_object()
        context['book_instances'] = BookInstance.objects.filter(book=book)
        context['available_instances'] = BookInstance.objects.filter(
            book=book, 
            status__exact='a'
        ).count()

        return context
from django.http import Http404    

def book_detail_view(request, pk):
    try:
        book_id = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404
    return render(
        request,
        'catalog/book_detail.html',
        context={'book':book_id,}
    )