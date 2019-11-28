from django.db import models
from django.urls import reverse  # Genrate urls by reversing the url pattern
import uuid  # REquired for unique book instance
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    """ Model representing a book genre. """
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """ String to represent the model """
        return self.name


class Book(models.Model):
    """ Model repr of a Book. """
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">\
                            ISBN number</a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a Genre for this book')

    def display_genre(self):
        """ Create a string for the Genre. This is required to display in Admin """
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def __str__(self):
        """ String repr of the book """
        return self.title

    def get_absolute_url(self):
        """ Returns the url to access a detailed record of this book """
        return reverse('book-detail', args=[str(self.id)])


class Language(models.Model):
    """ Model representing a language. """
    name = models.CharField(max_length=200,
                            help_text='Enter the book\'s natural language.')

    def __str__(self):
        """ String to represent the Model object """
        return self.name


class BookInstance(models.Model):
    """ Model representing a specific copy of a book (i.e. that can be borrowed from the library). """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On load'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability'
    )

    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),)
        ordering = ['due_back']
    
    @property
    def is_overdue(self):
        return self.due_back and date.today() > self.due_back

    def display_name(self):
        """ Used to display the name of the book for the Admin page. """
        return self.book.title

    def __str__(self):
        """ String repr of the book instance """
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """ Model repr an Author. """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """ Returns the url to access a particular author instance. """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """ String representing the Model Object. """
        return f'{self.last_name}, {self.first_name}'
