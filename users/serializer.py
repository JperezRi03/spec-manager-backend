from rest_framework import serializers
from .models import Book,Loan,Reader

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ["loan_date", "return_date"]

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
        loan = Loan.objects.create(**validated_data)
        return loan

    def update(self, instance, validated_data):
        returned = validated_data.get("returned", instance.returned)

        #Si se marca como devuelto vuelve a estar disponible
        if returned and not instance.returned:
            instance.book.status = "available"
            instance.book.save()
        elif returned and instance.returned:
            #No se puede devolver dos veces 
            raise serializers.ValidationError({
                "loan" : "Este prestamo ya fue devuelto anteriormente."
            })

        return super().update(instance, validated_data)




class BookSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Book
        fields = '__all__'


class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = '__all__'