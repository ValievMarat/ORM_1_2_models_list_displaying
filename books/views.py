import datetime

from django.core.paginator import Paginator
from django.shortcuts import render

from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {'books': books}
    return render(request, template, context)


def books_view_pub_date(request, pub_date):
    p_date = datetime.datetime.strptime(pub_date, '%Y-%m-%d')

    list_date = []
    list_values = Book.objects.order_by('pub_date').distinct('pub_date')
    for obj in list_values:
        list_date.append(datetime.datetime.strftime(obj.pub_date, '%Y-%m-%d'))

    page_number = list_date.index(pub_date) + 1

    paginator = Paginator(list_date, 1)
    page = paginator.get_page(page_number)

    if page_number < len(list_date):
        next_text = list_date[page_number]
    else:
        next_text = ''

    if page_number > 1:
        prev_text = list_date[page_number-2]
    else:
        prev_text = ''

    template = 'books/books_pub_date.html'
    books = Book.objects.all().filter(pub_date=p_date)
    context = {'books': books,
               'page': page,
               'next_text': next_text,
               'prev_text': prev_text}

    return render(request, template, context)
