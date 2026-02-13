from django.db import models
from django.conf import settings
from employees.models import Employee
from vehicles.models import Vehicle
from vendors.models import Vendor

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Fuel', 'Fuel'),
        ('Vendor', 'Vendor Payment'),
        ('General', 'General Office'),
    ]
    
    PAYMENT_CHOICES = [
        ('Cash', 'Cash'),
        ('Bank', 'Bank Transfer'),
        ('M-Pesa', 'M-Pesa'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    fuel_liters = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    odometer_reading = models.PositiveIntegerField(null=True, blank=True)

    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    # Relationships
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses_submitted')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses_approved')
    
    related_vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    related_vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    
    receipt = models.FileField(upload_to='receipts/%Y/%m/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} - {self.amount} ({self.status})"

    class Meta:
        ordering = ['-date']