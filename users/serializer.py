from rest_framework import serializers
from .models import Book,Loan,Reader

class BookSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Book
        fields = '__all__'

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = '__all__'