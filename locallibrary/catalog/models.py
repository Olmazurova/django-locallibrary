import uuid

from django.db import models
from django.urls import reverse

class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction, Non Fiction)', verbose_name='Название')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.).
        """
        return self.name


class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=200, verbose_name='Название книги')
    author = models.ForeignKey(
        'Author',
        on_delete=models.SET_NULL,
        null=True,
        # related_name='%(class)s_author',
        verbose_name='Автор книги'
    )
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book', verbose_name='Описание книги')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href-"https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book', verbose_name='Жанр')

    class Meta:
        verbose_name = 'книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('book_detail', args=[str(self.id)])

    def display_genre(self):
        """
        Creates a string for the Genre. This is requires to display genre in Admin.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Жанр'


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book.
    """

    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, verbose_name='Книга')
    imprint = models.CharField(max_length=200, verbose_name='Издательство')
    due_back = models.DateField(null=True, blank=True, verbose_name='Дата возврата')

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reversed'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability', verbose_name='Статус')

    class Meta:
        ordering = ['due_back']
        verbose_name = 'экземпляр'
        verbose_name_plural = 'Экземпляры книг'

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    date_of_death = models.DateField(null=True, blank=True, verbose_name='Дата смерти')
    # written_books = models.ManyToManyField(Book, verbose_name='Книги')

    class Meta:
        verbose_name = 'автор'
        verbose_name_plural = 'Авторы'
        ordering = ['last_name']

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author_detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return f'{self.last_name}, {self.first_name}'


class Language(models.Model):
    """
    Model representing a language.
    """
    name = models.CharField(max_length=200,
                            unique=True,
                            help_text="Enter the book's natural language (e.g. English, Russian)",
                            verbose_name='Язык')

    class Meta:
        verbose_name = 'язык'
        verbose_name_plural = 'Языки'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('language_detail', args=[str(self.id)])