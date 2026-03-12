from django.contrib import admin
from .models import Book, BorrowRecord

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_available', 'added_date')
    search_fields = ('title', 'author', 'isbn')

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'due_date', 'is_returned', 'return_date')
    list_filter = ('is_returned', 'borrow_date')