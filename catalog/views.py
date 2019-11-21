from django.shortcuts import render

# Create your views here.
from catalog.models import *
from django.views import generic


def index(request):
    """ View function for home page of site. """

    #  Number of visits
    num_visits = request.session.get('num_visits', 0) + 1
    request.session['num_visits'] = num_visits

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    #  Number of sci fi books
    num_sci_fi = Genre.objects.filter(name__exact='Science-Fiction').count()

    # Number of books that contains the word "Ellana"
    num_books_ellana = Book.objects.filter(title__icontains='Ellana').count()

    # The 'all()' is implied by default
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_sci_fi': num_sci_fi,
        'num_books_ellana': num_books_ellana,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book

    #  paginate_by = 2  # Paginate every 2

    # context_object_name = 'My book list'
    # queryset = Book.objects.filter(title__icontains='war')[:5]  # 5 books that contains war in the title
    # template_name = 'books/some_random_template.html'

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        #  You can add some data
        # context['any_data'] = "Some piece of data"
        return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author
