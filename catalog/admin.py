from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language


# Register your models here.

# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(Book)
# admin.site.register(BookInstance)
admin.site.register(Language)




@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',
                     'date_of_birth', 'date_of_death')
    list_filter = ('last_name', 'first_name')
    search_fields = ('last_name', 'first_name')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    list_filter = ('author', 'genre')
    search_fields = ('title', 'author__last_name')
    inlines = [BooksInstanceInline]
    
    def display_genre(self, obj):
        return ', '.join(genre.name for genre in obj.genre.all()[:3])
    display_genre.short_description = 'Genre'

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )


# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'display_genre')
#     list_filter = ('author', 'genre')
    
#     # def display_genre(self, obj):
#     #     """Создает строку для жанров (ManyToMany field)"""
#     #     return ', '.join(genre.name for genre in obj.genre.all()[:3])
#     # display_genre.short_description = 'Genre'

# class BookInstanceAdmin(admin.ModelAdmin):
#     list_display = ('book', 'status', 'due_back')
#     list_filter = ('status', 'due_back')
#     fieldsets = (
#         (None, {
#             'fields': ('book', 'imprint', 'id')
#         }),
#         ('Availability', {
#             'fields': ('status', 'due_back')
#         }),
#     )

# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     pass 

# @admin.register(BookInstance)
# class BookInstanceAdmin(admin.ModelAdmin):
#     pass

# admin.site.register(Author, AuthorAdmin)
# admin.site.register(Book, BookAdmin)
# admin.site.register(BookInstance, BookInstanceAdmin)
# admin.site.register(Genre)
