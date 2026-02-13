from django import forms
from .models import Vendor, VendorPayment

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = [
            'name', 'vendor_type', 'contact_person', 'phone_number', 
            'email', 'physical_address', 'registration_number'
        ]
        # This is where attributes (attrs) MUST live for ModelForms
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl bg-slate-50', 'placeholder': 'Company Name'}),
            'vendor_type': forms.Select(attrs={'class': 'w-full p-3 border rounded-xl bg-slate-50'}),
            'contact_person': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl bg-slate-50'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl bg-slate-50'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-3 border rounded-xl bg-slate-50'}),
            'physical_address': forms.Textarea(attrs={'class': 'w-full p-3 border rounded-xl bg-slate-50', 'rows': 2}),
            'registration_number': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl bg-slate-50'}),
        }

class VendorPaymentForm(forms.ModelForm):
    class Meta:
        model = VendorPayment
        fields = ['amount', 'payment_method', 'reference_code', 'notes']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'w-full p-3 border rounded-xl bg-slate-50', 'placeholder': '0.00'}),
            'payment_method': forms.Select(attrs={'class': 'w-full p-3 border rounded-xl bg-slate-50'}),
            'reference_code': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-xl bg-slate-50', 'placeholder': 'M-Pesa / Bank Ref'}),
            'notes': forms.Textarea(attrs={'class': 'w-full p-3 border rounded-xl bg-slate-50', 'rows': 3}),
        }