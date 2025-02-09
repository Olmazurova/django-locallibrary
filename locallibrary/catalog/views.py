from django.shortcuts import render

from .models import Book, Author, BookInstance, Genre


def index(request):
    """
    Функция отображения домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Доступные книги (статус "а")
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    num_books_with_and = Book.objects.filter(title__contains=' и ').count()
    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_instances': num_instances,
            'num_istances_available': num_instances_available,
            'num_authors': num_authors,
            'num_genres': num_genres,
            'num_books_with_and': num_books_with_and,
        }
    )
