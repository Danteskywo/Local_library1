from django.shortcuts import render, get_object_or_404
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

    historyFive = historyFive_books(request)

    return render(
        request,'index.html',
        context={'num_books':num_books,
                 'num_instances':num_instances,
                 'num_instances_available':num_instances_available,
                 'num_authors':num_authors,
                 'num_genre':num_genre,
                 'num_visits':num_visits,
                 'historyFive_books': historyFive,}
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

        book_id = str(self, object.pk)
        recently_viewed = self.request.session.get(**kwargs)
        


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

def book_detail(request,pk):
    book = get_object_or_404(Book,pk=pk)
    view_id = request.session.get('recently_viewed',[])
    if pk_str in view_id:
        view_id.remove(pk_str)
    view_id.insert(0,pk_str)
    request.session['recently_viewed'] = view_id[:5]
    context = {
        'book':book,
        'book_instances': BookInstance.objects.filter(book=book),
        'available_instances':BookInstance.objects.filter(book=book, status_exact='a').count(),
    }
    return render(request, 'catalog/book_detail.html', context)
        # view_id=five_view_id[:5]
        # request.session['']



def historyFive_books(request):
    viewed_ids = request.session.get('recently_viewed', [])
    books = Book.objects.filter(id__in=viewed_ids)
    book_dict = {str(book.id): book for book in books}
    ordered_books = [book_dict[book_id] for book_id in viewed_ids if book_id in book_dict]
    return ordered_books



# Задание 1: Среднее - История просмотренных книг
# Цель: Научиться работать со списками в сессиях.
# Задача:
# Реализуйте функционал "недавно просмотренные книги"
# При переходе на страницу детальной информации о книге добавляйте
# ее ID в список recently_viewed в сессии
# Храните только последние 5 просмотренных книг
# На главной странице или в сайдбаре показывайте список недавно
# просмотренных книг

# Задание №2. Творческое - Система закладок
# Цель: Комплексное применение сессий.
# Задача:
# ● Реализуйте систему закладок для книг (без регистрации пользователей)
# ● Пользователь может добавлять/удалять книги в "Мои закладки"
# ● На отдельной странице показывать все книги из закладок
# ● Реализовать кнопку "Очистить все закладки"


# Задание №3. Аналитическое - Время сессии
# Цель: Работа с временными метками в сессиях.
# Задача:
# Записывать время первого визита пользователя на сайт
# Показывать сколько времени пользователь провел на 
# сайте (текущее время - время первого визита)
# Сбрасывать время при новом сеансе
# (когда пользователь закрывает и открывает браузер)


# Задание 4. Ограничение частоты запросов Цель:
# Защита от злоупотреблений с помощью сессий. Задача:
# Ограничить количество запросов к форме поиска
# (не более 10 в минуту)
# Хранить в сессии время последних запросов


# Доработка домашней страницы
# 1. В главном файле шаблона (base_generic.html)
# есть блок title. Переопределите этот блок в индексном шаблоне
# (index.html) и задайте новый заголовок для этой страницы.
# 2. Модифицируйте функцию отображения таким образом,
# чтобы получать из базы данных количество жанров и количество книг,
# которые содержат в своих заголовках какое-либо слово
# (без учёта регистра), а затем передайте эти значения в шаблон.


# Форматирование данных в шаблоне
# Задача: Используйте шаблонные фильтры для форматирования вывода:
# Название библиотеки "LocalLibrary" должно отображаться
# заглавными буквами
# Числовые значения должны форматироваться с разделителями
# тысяч (например, 1,234 вместо 1234)
# Добавьте текущую дату в формате "ДД.ММ.ГГГГ"


# Новый тип книги.
# Добавь для книг языки например Lang Английский.
# Выведите авторов на главную страницу у кого сколько книг
# на разных языках
# (например:
# Стороженко Ян Романович. Английские издания: 6. Русские издания: 4.)