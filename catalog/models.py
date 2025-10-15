
# Create your models here.
from django.db import models
from django.urls import reverse
import uuid
from django.db.models import UniqueConstraint #Уникальность ограничения
from django.db.models.functions import Lower


# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=100, help_text="Enter a book genre")

    def __str__(self):
        return self.name

class Language(models.Model):
    
    name = models.CharField(max_length=200,
                            unique=True,
                            help_text="Enter the book's natural language")

    def get_absolute_url(self):
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message = "Language already exists (case insensitive match)"
            ),
        ]


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Перейти к описанию")
    isbn = models.CharField('ISBN', max_length=13, help_text="ISBN Entr")
    genre = models.ManyToManyField('Genre', help_text="Select a genre for this book")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), help_text="Введите UUID")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'На обслуживании'),
        ('o', 'Выдана'),
        ('a', 'Доступна'),
        ('r', 'Зарезервирована'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True,
                     default='m', help_text='book Availability')
    
    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return '%s (%s)' % (self.id, self.book.title)

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_urls(self):
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        return '%s (%s)' % (self.last_name, self.first_name)
    
