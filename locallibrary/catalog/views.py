from django.shortcuts import render
from django.views import generic

from .models import Book, Author, BookInstance, Genre


class BookListView(generic.ListView):
    """Класс отображения, выводит список информации по книгам."""

    model = Book
    template_name = 'book_list.html' # путь где искать шаблон
    context_object_name = 'books' # указываем, чтобы имя отличалось от object_list или имямодели_list
    paginate_by = 5 # количество книг на странице

    def get_context_data(
        self, *, object_list = None, **kwargs
    ):
        """Метод добавляет в контекст дополнительную информацию"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список книг'
        return context

    def get_queryset(self):
        """
        Метод позволяет добавить не полностью всю информацию,
        а установить фильтры для неё.
        """
        return Book.objects.all()[:11]


class BookDetailView(generic.DetailView):
    """Обобщённый класс отображения для вывода информации по конкретной книге."""

    model = Book
    template_name = 'book_detail.html'


class AuthorListView(generic.ListView):
    """
    Класс отображения выводит список авторов, чьи книги имеются в библиотеке.
    """

    model = Author
    template_name = 'author_list.html'
    context_object_name = 'authors'
    paginate_by = 5

    def get_context_data(
        self, *, object_list = None, **kwargs
    ):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список авторов'
        return context


class AuthorDetailView(generic.DetailView):
    """
    Класс отображения выводит информацию о конкретном авторе.
    """

    model = Author
    template_name = 'author_detail.html'


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
    # Session
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_genres': num_genres,
            'num_books_with_and': num_books_with_and,
            'num_visits': num_visits,
        }
    )
