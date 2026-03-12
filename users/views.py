from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from books.models import BorrowRecord

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('users:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    current_borrows = BorrowRecord.objects.filter(user=request.user, is_returned=False)
    history_borrows = BorrowRecord.objects.filter(user=request.user, is_returned=True)
    return render(request, 'users/profile.html', {
        'current_borrows': current_borrows,
        'history_borrows': history_borrows
    })