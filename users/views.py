from django.shortcuts import render
from rest_framework import viewsets
from .models import Book, Loan, Reader
from .serializer import BookSerializer, LoanSerializer, ReaderSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
# Create your views here.
