import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse, reverse_lazy

from .forms import RenewBookForm
from .models import Book, Author, BookInstance, Genre


class BookListView(ListView):
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


class BookDetailView(DetailView):
    """Обобщённый класс отображения для вывода информации по конкретной книге."""

    model = Book
    template_name = 'book_detail.html'


class AuthorListView(ListView):
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


class AuthorDetailView(DetailView):
    """
    Класс отображения выводит информацию о конкретном авторе.
    """

    model = Author
    template_name = 'author_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """
    Базовый класс представления списка взятых книг текущего пользователя.
    """
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user
        ).filter(
            status__exact='o'
        ).order_by('due_back')


class LoanedAllBooksListView(LoginRequiredMixin, ListView):
    """
    Базовый класс представления списка всех взятых книг в библиотеке.
    """
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            Q(status__exact='o') | Q(status__exact='m')
        ).order_by('due_back')


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '12/10/2016',}  # начальное значение поля в форме


class AuthorUpdate(UpdateView):
    model = Author
    fields = [
        'first_name',
        'last_name',
        'date_of_birth',
        'date_of_death',
    ]


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


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


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    Представление формы для изменения библиотекарем
    даты возврата экземпляра книги.
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':
        # Создаём экземпляр формы и заполняем данными из запроса (связывние, binding)
        form = RenewBookForm(request.POST)

        # Проверка валидности
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            # (здесь мф просто присваиваем их полю due_back)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # Переход по адресу 'all_borrowed':
            return HttpResponseRedirect(reverse('all_borrowed'))

    # Если это GET (или другой запрос), создать форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

        return render(
            request,
            'catalog/book_renew_librarian.html',
            {'form': form, 'bookinst': book_inst,}
        )

