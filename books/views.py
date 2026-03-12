from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import timedelta
from .models import Book, BorrowRecord

def is_admin(user):
    return user.is_staff

def catalog(request):
    books = Book.objects.all()
    query = request.GET.get('q')
    if query:
        books = books.filter(title__icontains=query)
    return render(request, 'books/catalog.html', {'books': books})

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/detail.html', {'book': book})

@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not book.is_available:
        messages.error(request, "This book is currently unavailable.")
        return redirect('books:catalog')
    
    if BorrowRecord.objects.filter(user=request.user, book=book, is_returned=False).exists():
        messages.error(request, "You have already borrowed this book.")
        return redirect('books:catalog')

    BorrowRecord.objects.create(
        user=request.user,
        book=book,
        due_date=timezone.now() + timedelta(days=14) # Assuming the loan period is 14 days.
    )
    book.is_available = False
    book.save()
    messages.success(request, f"You have successfully borrowed '{book.title}'.")
    return redirect('users:profile')

@login_required
def return_book(request, record_id):
    record = get_object_or_404(BorrowRecord, id=record_id, user=request.user)
    if record.is_returned:
        messages.error(request, "This book has already been returned.")
        return redirect('users:profile')
        
    record.return_date = timezone.now()
    record.is_returned = True
    record.save()

    # Set the book status to "Available".
    record.book.is_available = True
    record.book.save()

    messages.success(request, f"Successfully returned '{record.book.title}'.")
    return redirect('users:profile')

@user_passes_test(is_admin)
def admin_dashboard(request):
    # Retrieve all records of items not yet returned
    active_borrows = BorrowRecord.objects.filter(is_returned=False)
    # Get overdue records.
    overdue_borrows = active_borrows.filter(due_date__lt=timezone.now())
    
    # Get the total number of books and the number currently checked out
    total_books = Book.objects.count()
    borrowed_books = BorrowRecord.objects.filter(is_returned=False).count()
    
    context = {
        'active_borrows': active_borrows,
        'overdue_borrows': overdue_borrows,
        'total_books': total_books,
        'borrowed_books': borrowed_books,
    }
    return render(request, 'books/admin_dashboard.html', context)

@user_passes_test(is_admin)
def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        isbn = request.POST['isbn']
        description = request.POST.get('description', '') 

        cover_image = None
        if 'cover_image' in request.FILES:
            cover_image = request.FILES['cover_image']
        
        book = Book.objects.create(
            title=title,
            author=author,
            isbn=isbn,
            description=description,
            cover_image=cover_image
        )
        
        messages.success(request, f'Book "{title}" has been added successfully.')
        return redirect('books:admin_dashboard')
    
    return redirect('books:admin_dashboard')

@user_passes_test(is_admin)
def remove_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    title = book.title
    book.delete()
    messages.success(request, f"Book '{title}' has been removed successfully.")
    return redirect('books:admin_dashboard')