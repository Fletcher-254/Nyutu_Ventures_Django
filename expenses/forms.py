# expenses/forms.py
from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'date', 'amount', 'category', 'description', 
            'payment_method', 'related_vehicle', 'related_vendor', 'receipt'
        ]
        widgets = {
            # Use 'datetime-local' so the browser provides a picker
            'date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'w-full p-3 border rounded-xl bg-slate-50'},
                format='%Y-%m-%dT%H:%M'
            ),
            'amount': forms.NumberInput(attrs={'class': 'w-full p-3 border rounded-xl bg-slate-50', 'placeholder': '0.00'}),
            'category': forms.Select(attrs={'class': 'w-full p-3 border rounded-xl bg-slate-50'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-3 border rounded-xl bg-slate-50', 'rows': 3, 'placeholder': 'What was this for?'}),
            'payment_method': forms.Select(attrs={'class': 'w-full p-3 border rounded-xl bg-slate-50'}),
            'related_vehicle': forms.Select(attrs={'class': 'w-full p-3 border rounded-xl bg-slate-50'}),
            'related_vendor': forms.Select(attrs={'class': 'w-full p-3 border rounded-xl bg-slate-50'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure date is formatted correctly for the HTML5 input when editing
        if self.instance and self.instance.date:
            self.initial['date'] = self.instance.date.strftime('%Y-%m-%dT%H:%M')