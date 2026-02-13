from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'date', 'amount', 'category', 'description', 
            'payment_method', 'related_vehicle', 'related_vendor', 
            'fuel_liters', 'odometer_reading', 'receipt'
        ]
        widgets = {
            'date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'w-full p-3 border border-slate-200 rounded-xl bg-slate-50 focus:ring-2 focus:ring-blue-500 outline-none transition-all'},
                format='%Y-%m-%dT%H:%M'
            ),
            'amount': forms.NumberInput(attrs={'class': 'w-full p-3 border border-slate-200 rounded-xl bg-slate-50', 'placeholder': '0.00'}),
            'category': forms.Select(attrs={'id': 'id_category', 'class': 'w-full p-3 border border-slate-200 rounded-xl bg-slate-50'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-3 border border-slate-200 rounded-xl bg-slate-50', 'rows': 3, 'placeholder': 'Provide details...'}),
            'payment_method': forms.Select(attrs={'class': 'w-full p-3 border border-slate-200 rounded-xl bg-slate-50'}),
            'related_vehicle': forms.Select(attrs={'class': 'w-full p-3 border border-slate-200 rounded-xl bg-slate-50'}),
            'related_vendor': forms.Select(attrs={'class': 'w-full p-3 border border-slate-200 rounded-xl bg-slate-50'}),
            'fuel_liters': forms.NumberInput(attrs={'class': 'w-full p-3 border border-slate-200 rounded-xl bg-slate-50', 'placeholder': 'Liters'}),
            'odometer_reading': forms.NumberInput(attrs={'class': 'w-full p-3 border border-slate-200 rounded-xl bg-slate-50', 'placeholder': 'Current KM'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.date:
            self.initial['date'] = self.instance.date.strftime('%Y-%m-%dT%H:%M')