from django import forms
from .models import Book

class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'description', 'cover_image']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'cover_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }