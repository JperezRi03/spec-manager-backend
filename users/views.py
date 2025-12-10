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
    @action(detail=True, methods=['post'])
    def loan(self, request, pk=None):
        book = self.get_object()

        #Verificar disponibilidad
        if book.status != "available":
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
        
        try:
            reader = Reader.objects.get(id = reader_id)
        except Reader.DoesNotExist:
            return Response(
                {"error":"El lector no existe."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        #5. Crear el prestamo
        loan = Loan.objects.create(
            book=book,
            reader=reader
        )

        #Cambiar el estado del libro
        book.status = "unavailable"
        book.save()

        return Response(
            {"message0":"Libro prestado con exito","loan_id":loan.id},
            status=status.HTTP_201_CREATED
        )

    # POST /books/<id>/return/
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        book = self.get_object()

        #Prestamo Activo
        active_loan = Loan.objects.filter(book=book, returned=False).first()
        if not active_loan:
            return Response(
                {"error":"No existe un prestamo activo para este libro"},
                status=status.HTTP_400_BAD_REQUEST
            )

        #Evitar devolver dos veces.
        if active_loan.returned:
            return Response(
                {"error":"Este libro ya fue devuelto anteriormente"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        #Marcar Devolucion.
        active_loan.returned = True
        active_loan.return_date = timezone.now()
        active_loan.save()

        #Cambiar estado del libro
        book.status = "available"
        book.save()

        return Response(
            {"message":"Libro devuelto correctamente"},
            status = status.HTTP_200_OK
        )

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class ReaderViewSet(viewsets.ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
# Create your views here.
