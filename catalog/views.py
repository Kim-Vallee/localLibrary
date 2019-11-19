from django.shortcuts import render

# Create your views here.
from catalog.models import *
from django.views import generic


def index(request):
    """ View function for home page of site. """

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'My book list'
    queryset = Book.objects.filter(title__icontains='war')[:5]  # 5 books that contains war in the title
    template_name = 'books/some_random_template.html'


