from django.http import HttpResponse
from django.utils.dateparse import parse_datetime

from .models import Author, Book, Loan

def q1_all_authors(request):
    query_set = Author.objects.all()
    # Code to do the query above followed by this output loop
    output = "<ul>"
    for obj in query_set:
        output += f"<li>{obj}</li>"
    output += "</ul>"
    return HttpResponse(output)

def q2_all_books(request):
    query_set = Book.objects.all().order_by('-published_year')
    # Code to do the query above followed by this output loop
    output = "<ul>"
    for obj in query_set:
        output += f"<li>{obj}</li>"
    output += "</ul>"
    return HttpResponse(output)

def q3_books_after_year(request, year):
    query_set = Book.objects.filter(published_year__gt=year).order_by('published_year')
    # Code to do the query above followed by this output loop
    output = "<ul>"
    for obj in query_set:
        output += f"<li>{obj}</li>"
    output += "</ul>"
    return HttpResponse(output)

def q4_books_by_author(request, author_id):
    query_set = Book.objects.filter(author=author_id)
    # Code to do the query above followed by this output loop
    output = "<ul>"
    for obj in query_set:
        output += f"<li>{obj}</li>"
    output += "</ul>"
    return HttpResponse(output)

def q5_open_loans(request):
    query_set = Loan.objects.filter(returned=False)
    # Code to do the query above followed by this output loop
    output = "<ul>"
    for obj in query_set:
        output += f"<li>{obj.borrower_name, obj.book.title}</li>"
    output += "</ul>"
    return HttpResponse(output)

def q6_loans_due_before(request):
    try:
        time_str = request.GET.get("t")

        if not time_str:
            return HttpResponse("<h1>ERROR: Please provide a time parameter.</h1>")

        time = parse_datetime(time_str)
        if time is None:
            return HttpResponse("<h1>ERROR: Invalid datetime format.</h1>")
        query_set = Loan.objects.filter(due_at__lt=time)
        output = "<ul>"
        for obj in query_set:
            output += f"<li>{obj.borrower_name, obj.book.title}</li>"
        output += "</ul>"
        return HttpResponse(output)
    except ValueError as e:
        return HttpResponse(f"<h1>Error found: {e}</h1>")

def q7_book_by_isbn(request, isbn):
    query_set = Book.objects.filter(isbn=isbn)
    if query_set.count() == 0:
        return HttpResponse("<h1>No matching book found.</h1>")
    # Code to do the query above followed by this output loop
    output = "<ul>"
    for obj in query_set:
        output += f"<li>{obj}</li>"
    output += "</ul>"
    return HttpResponse(output)

def q8_stats(request):
    book_count = Book.objects.all().count()
    author_count = Author.objects.all().count()
    loan_count = Loan.objects.all().count()
    open_loan_count = Loan.objects.filter(returned=False).count()

    return HttpResponse(f"<p>number of books: {book_count}</p><p>number of authors: {author_count}</p><p>number of loans: {loan_count}</p><p>number of open loans: {open_loan_count}</p>")
