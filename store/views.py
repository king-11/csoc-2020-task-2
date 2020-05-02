from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def index(request):
    return render(request, 'store/index.html')


def bookDetailView(request, bid):
    book = get_object_or_404(Book, pk=bid)

    if request.method == "POST":
        user = request.user
        rating = request.POST['rating']
        try:
            changeRating = BookRating.objects.get(book=book, username=user)
        except ObjectDoesNotExist:
            changeRating = BookRating.objects.create(book=book, username=user)
        finally:
            changeRating.rating = rating
            changeRating.save()

    book.rating = BookRating.objects.filter(
        book=book).aggregate(rating=Avg('rating'))['rating']

    book.save()

    context = {
        'book': None,
        'num_available': None,
    }
    if request.user.is_authenticated:
        try:
            context['user_review'] = BookRating.objects.get(
                book=book, username=request.user).rating
        except ObjectDoesNotExist:
            context['user_review'] = None

    context['num_available'] = BookCopy.objects.filter(
        book=book, status=True).count()
    context['book'] = book
    template_name = 'store/book_detail.html'

    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    context = {
        'books': None,
    }
    get_data = request.GET

    if get_data:
        context['books'] = Book.objects.filter(
            title__icontains=get_data['title'], author__icontains=get_data['author'], genre__icontains=get_data['genre']
        )
    else:
        context['books'] = Book.objects.all()

    return render(request, template_name, context=context)


@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    context = {
        'books': None,
    }
    user = request.user
    books = BookCopy.objects.filter(borrower=user)
    context['books'] = books
    return render(request, template_name, context=context)


@csrf_exempt
@login_required
def loanBookView(request):
    response_data = {
        'message': None,
    }
    bid = request.body.decode("utf-8").split("=")[1]
    book = BookCopy.objects.get(book_id=bid, status=True)

    if book:
        book.borrower = request.user
        book.borrow_date = timezone.datetime.today().date()
        book.status = False
        book.save()
        response_data['message'] = 'success'
    else:
        response_data['message'] = 'failure'
    return JsonResponse(response_data)


@csrf_exempt
@login_required
def returnBookView(request):
    response_data = {
        'message': None,
    }

    bid = request.body.decode("utf-8").split("=")[1]
    book = get_object_or_404(BookCopy, pk=bid)

    if book:
        book.borrower = None
        book.borrow_date = None
        book.status = True
        book.save()
        response_data['message'] = 'success'
    else:
        response_data['message'] = 'failure'
    return JsonResponse(response_data)
