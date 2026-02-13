from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'category', 'amount', 'status', 'submitted_by', 'related_vehicle')
    list_filter = ('category', 'status', 'date', 'related_vehicle', 'related_vendor')
    search_fields = ('description', 'submitted_by__email', 'related_vehicle__plate_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Info', {'fields': ('date', 'amount', 'category', 'description', 'payment_method')}),
        ('Status & Approval', {'fields': ('status', 'submitted_by', 'approved_by')}),
        ('Linking', {'fields': ('related_vehicle', 'related_vendor', 'receipt')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )