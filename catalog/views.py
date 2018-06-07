from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BookInstance, Genre

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # Метод 'all()' применен по умолчанию.
    num_genres = Genre.objects.all().count()
    num_books_for_managers = Book.objects.filter(title__icontains='руковод').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    
    # Отрисовка HTML-шаблона index.html с данными внутри 
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_books':num_books,
                 'num_instances':num_instances,
                 'num_instances_available':num_instances_available,
                 'num_authors':num_authors,
                 'num_genres':num_genres,
                 'num_books_for_managers':num_books_for_managers,
                 'num_visits':num_visits,}
    )


from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 3

    # Examples modifying view using attributes
    # context_object_name = 'my_book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location

    # Examples modifying view using finction
    # get_queryset() more flexible than just attribute "queryset" but you don't have really profit
    # def get_queryset(self):
        # return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    # We might also override get_context_data() in order to pass additional context variables to the template
    # def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        # context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        # context['some_data'] = 'This is just some data'
        # return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksByAllUsersListView(PermissionRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_by_all_users.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


# Class - working with forms
from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed-books') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


# The lesson about creating a form using generic view
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# The "create" and "update" views use the same template by default, 
# which will be named after your model: model_name_form.html 
# (you can change the suffix to something other than _form 
# using the template_name_suffix field in your view, e.g. template_name_suffix = '_other_suffix')

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_birth':'1970-01-30',}
    # Добавил, т.к. было в обучении, но сам обошёл в HTML шаблоне
    permission_required = 'catalog.can_mark_returned'

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

# The "delete" view expects to find a template named with the format model_name_confirm_delete.html 
# (again, you can change the suffix using template_name_suffix in your view)

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

# The views for Book forms
class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    # Just commented "initial" because don't have ideas now
    # initial={'date_of_birth':'1970-01-30',}

class BookUpdate(UpdateView):
    model = Book
    # Don't have ideas now for specific book's fields so add them all
    # fields = ['first_name','last_name','date_of_birth','date_of_death']
    fields = '__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')




















