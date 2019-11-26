import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from catalog.forms import RenewBookForm
from catalog.models import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """ Generic class-based view listing books on loan to the current user. """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


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


class LoanedBooksLibrarianListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_librarian.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If it is a post request we proceed
    if request.method == "POST":

        # Create a form instance that we populate with data
        form = RenewBookForm(request.POST)

        # Check form validity
        if form.is_valid():
            # We process the data
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # Redirect to a new URL
            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)
