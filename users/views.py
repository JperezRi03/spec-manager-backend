from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Book, Loan, Reader
from .serializer import BookSerializer, LoanSerializer, ReaderSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # POST /books/<ID>/loan
    @action(detaill=True, methods=['post'])
    def loan(self, request, pk=None):
        book = self.get_object()

        #Verificar disponibilidad
        if book.status != "Available":
            return Response(
                {"error" : "El libro no esta disponible para prestamo"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        #Verificar si hay prestamos activos
        active_loan = Loan.objects.filter(book=book, returned = False).first()
        if active_loan:
            return Response(
                {"error":"Este libro ya se encuentra en prestamo"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
        #Validar si viene reader_id en la peticion

        reader_id = request.data.get("reader_id")
        if not reader_id:
            return Response(
                {"Error":"No se capturo el reader_id"},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
# Create your views here.
