from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin","Admin"),
        ("librerian","Librerian"),
        ("reader","Reader")
    ]
    role = models.CharField(max_length=20,choices=ROLE_CHOICES, default="reader")
    
    def __str__(self):
        return f"{self.username} ({self.role})"


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    published_year = models.IntegerField()
    isbn = models.CharField(max_length=13, unique=True)
    status = models.CharField(
    max_length=20,
    choices=[
        ("available", "Disponible"),
        ("unavailable", "No disponible temporalmente"),
        ("lost", "Perdido"),
        ("internal", "Uso interno"),
    ],
    default="available")
    status_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.isbn})"

class Reader(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Loan(models.Model): #Relacion de prestamos entre los libros y lo lectores#
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    returned = models.BooleanField(default=False)

    # Auditoría
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_loans"
    )

    returned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="returned_loans"
    )