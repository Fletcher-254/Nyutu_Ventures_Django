from django.db import models
from django.conf import settings
from django.utils import timezone

class Employee(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    id_number = models.CharField(max_length=50, unique=True, null=True)
    next_of_kin_name = models.CharField(max_length=255, null=True)
    next_of_kin_phone = models.CharField(max_length=20, null=True)
    passport_photo = models.ImageField(upload_to='employees/photos/', null=True, blank=True)
    salary_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Soft Delete & Timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class EmployeeHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50) # e.g., "Created", "Updated", "Soft Deleted"
    changes = models.TextField(null=True, blank=True) # Description of what changed
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('employee', 'date')     


# employees/models.py additions
class EmployeeAccount(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='payroll_account')
    total_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    @property
    def balance_due(self):
        return self.total_earned - self.total_paid

class Payment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference_number = models.CharField(max_length=100, unique=True) # M-Pesa Receipt No.
    date_paid = models.DateTimeField(auto_now_add=True)
    paid_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.employee.name} - KES {self.amount}"        

     