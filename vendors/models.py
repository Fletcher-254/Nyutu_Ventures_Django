from django.db import models
from django.conf import settings
from decimal import Decimal

class Vendor(models.Model):
    TYPE_CHOICES = [
        ('Supplier', 'Supplier'),
        ('Contractor', 'Contractor'),
        ('Service Provider', 'Service Provider'),
    ]
    
    name = models.CharField(max_length=255)
    vendor_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    contact_person = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    physical_address = models.TextField(blank=True, null=True)
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class VendorAccount(models.Model):
    STATUS_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Partially Paid', 'Partially Paid'),
        ('Paid', 'Paid'),
    ]
    
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, related_name='account')
    total_owed = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    last_payment_date = models.DateTimeField(null=True, blank=True)

    @property
    def current_balance(self):
        return self.total_owed - self.total_paid

    @property
    def status(self):
        balance = self.current_balance
        if balance <= 0:
            return 'Paid'
        elif self.total_paid > 0:
            return 'Partially Paid'
        return 'Unpaid'

    def __str__(self):
        return f"Account: {self.vendor.name}"

class VendorPayment(models.Model):
    METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('M-Pesa', 'M-Pesa'),
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=METHOD_CHOICES)
    reference_code = models.CharField(max_length=100, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Update Vendor Account on save
        account = self.vendor.account
        account.total_paid += Decimal(self.amount)
        account.last_payment_date = self.payment_date
        account.save()
        super().save(*args, **kwargs)