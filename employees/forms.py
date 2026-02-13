import re
from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add asterisks to required fields
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].label = f"{self.fields[field].label} *"

    class Meta:
        model = Employee
        fields = ['name', 'id_number', 'phone', 'salary_per_day', 'passport_photo']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone').replace(" ", "")
        # Regex for Kenyan formats: +254..., 254..., 07..., or 01...
        kenyan_regex = r'^(?:\+254|254|0)?(7|1)[0-9]{8}$'
        
        if not re.match(kenyan_regex, phone):
            raise forms.ValidationError("Enter a valid Kenyan number (e.g., 0712345678 or +254712345678).")
        
        # Normalize to 254... format for M-Pesa API compatibility
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        elif phone.startswith('+'):
            phone = phone[1:]
        elif not phone.startswith('254'):
            phone = '254' + phone
            
        return phone