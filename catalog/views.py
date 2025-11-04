from django.shortcuts import render, get_object_or_404
from .models import Book, BookInstance, Author, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import RenewBookForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



# Create your views here.
class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/all_borrowed_books.html'
    context_object_name = 'borrowed_books'
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')



class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):

    model = BookInstance
    template_name ='bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user).filter(
                status__exact='o').order_by('due_back')

class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        # ваша логика для GET запроса
        return render(request, 'template_name.html')
    
    def post(self, request):
        # ваша логика для POST запроса
        pass

@login_required
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
   
    num_books=Book.objects.all().count()

    num_instances=BookInstance.objects.all().count()
    
    # Доступные книги (статус = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    
    num_authors=Author.objects.count()

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






@login_required
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

@login_required
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

@login_required
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
        context = super().get_context_data(**kwargs)

        book_id = self.object.pk
        recently_viewed = self.request.session.get('recently_viewed', [])
        


        book = self.get_object()
        if book:
            context['book_instances'] = BookInstance.objects.filter(book=book)
            context['available_instances'] = BookInstance.objects.filter(
                book=book, 
                status__exact='a'
            ).count()

        return context
    
    
from django.http import Http404    
@login_required
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
@login_required
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

@login_required
@permission_required('catalog.can_mark_returned')
def historyFive_books(request):
    viewed_ids = request.session.get('recently_viewed', [])
    books = Book.objects.filter(id__in=viewed_ids)
    book_dict = {str(book.id): book for book in books}
    ordered_books = [book_dict[book_id] for book_id in viewed_ids if book_id in book_dict]
    return ordered_books

def renew_book_librarian(request, pk):

    book_inst = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

    



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