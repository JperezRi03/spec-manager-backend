from rest_framework import serializers
from django.utils import timezone
from .models import Book,Loan,Reader

class LoanSerializer(serializers.ModelSerializer):

    book_detail = serializers.SerializerMethodField()
    reader_detail = serializers.SerializerMethodField()
    created_by = serializers.StringRelatedField(read_only=True)
    returned_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = [
            "loan_date",
            "return_date",
            "created_by",
            "returned_by",
        ]


    def validate(self, data):
        book = data["book"]
        reader = data["reader"]

        #Validar disponibillidad  del libro 
        if book.status != "available":
            raise serializers.ValidationError({
                "book": "Este libro no esta disponible para un prestamo"
            })
        
        #Validar si hay un prestamo activo.
        active_loan = Loan.objects.filter(book=book, returned=False).exists()
        if active_loan:
            raise serializers.ValidationError({
                "book" : "Este libro ya tiene un prestamo actualmente"
            })
        
        #Validar si el lector esta activo
        if not reader.is_active: 
            raise serializers.ValidationError({
                "reader" : "Este lector no esta activo"
            })
        
        return data
    
    #Crear Prestamos
    def create(self, validated_data):
        book = validated_data["book"]

        #Cuando se presta el libro el estado cambia
        book.status = "unavailable"
        book.save()
        return Loan.objects.create(**validated_data)
    
    #Actualizar Prestamo
    def update(self, instance, validated_data):
        mark_as_returned = validated_data.get("returned", instance.returned)

        #Si se marca como devuelto vuelve a estar disponible
        if mark_as_returned:
            #Ya estaba devuelto.
            if instance.returned:
                raise serializers.ValidationError({
                    "loan" : "Este prestamo ya fue devuelto anteriormente."
                })

            # Actualizamos
            instance.returned = True
            instance.return_date = timezone.now()

            # Libro vuelve a estar disponible
            instance.book.status = "available"
            instance.book.save()

        return super().update(instance, validated_data) 

    def get_book_detail(self,obj):
        return{
            "id": obj.book.id,
            "title": obj.book.title,
            "author": obj.book.author
        }
    
    def get_reader_detail(self, obj):
        return {
            "id": obj.reader.id,
            "name": f"{obj.reader.first_name} {obj.reader.last_name}"
        }

class BookSerializer(serializers.ModelSerializer):
    current_loan = serializers.SerializerMethodField()
    current_reader = serializers.SerializerMethodField()

    class Meta: 
        model = Book
        fields = '__all__'

    def get_current_loan(self,obj):
        loan = Loan.objects.filter(book=obj, returned=False).first()
        if loan:
            return LoanSerializer(loan).data
        return None

    def get_current_reader(self,obj):
        loan = Loan.objects.filter(book=obj, returned=False).first()
        if loan:
            reader = loan.reader
            return{
                "id": reader.id,
                "name": f"{reader.first_name} {reader.last_name}"
            }

class ReaderSerializer(serializers.ModelSerializer):
    loans = serializers.SerializerMethodField()
    
    class Meta:
        model = Reader
        fields = '__all__'

    def get_loans(self, obj):
        loans = Loan.objects.filter(reader=obj).order_by('-loan_date')
        return [
            {
                "id": loan.id,
                "book": loan.book.title,
                "returned": loan.returned,
                "loan_date": loan.loan_date,
                "return_date": loan.return_date
            }
            for loan in loans
        ]