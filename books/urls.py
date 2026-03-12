from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('<int:pk>/', views.book_detail, name='detail'),
    path('<int:pk>/borrow/', views.borrow_book, name='borrow'),
    path('return/<int:record_id>/', views.return_book, name='return'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/add/', views.add_book, name='add_book'),
    path('admin/remove/<int:book_id>/', views.remove_book, name='remove_book'),
]