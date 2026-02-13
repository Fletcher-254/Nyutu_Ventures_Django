from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from .models import Vendor, VendorAccount, VendorPayment
from .forms import VendorForm, VendorPaymentForm

@login_required
def vendor_detail(request, pk):
    """This was the missing piece causing your error"""
    vendor = get_object_or_404(Vendor, pk=pk)
    # We use getattr in case a vendor account hasn't been created yet
    account = getattr(vendor, 'vendoraccount', None)
    return render(request, 'vendors/vendor_detail.html', {
        'vendor': vendor,
        'account': account
    })


@login_required
def vendor_list(request):
    """
    The Master List: Shows ALL vendors.
    Accessible by both Admin and Director.
    """
    vendors = Vendor.objects.all().order_by('name')
    return render(request, 'vendors/vendor_list.html', {
        'vendors': vendors
    })

@login_required
def unpaid_vendors(request):
    """
    The Financial View: Only shows vendors with outstanding balances.
    Usually restricted to Director/Manager in your sidebar logic.
    """
    # Filter for accounts where balance is greater than 0
    accounts = VendorAccount.objects.filter(current_balance__gt=0).select_related('vendor').order_by('-current_balance')
    
    # Calculate the total debt across all vendors
    total_outstanding = accounts.aggregate(Sum('current_balance'))['current_balance__sum'] or 0
    
    return render(request, 'vendors/unpaid_vendors.html', {
        'accounts': accounts,
        'total_outstanding': total_outstanding
    })

@login_required
def record_payment(request, vendor_id):
    """
    Handles debt reduction.
    """
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    
    if request.method == 'POST':
        form = VendorPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.vendor = vendor
            payment.save()  # This triggers your signals to update the VendorAccount balance
            
            messages.success(request, f"Payment of KES {payment.amount:,.2f} recorded for {vendor.name}")
            return redirect('unpaid_vendors')
    else:
        form = VendorPaymentForm()
        
    return render(request, 'vendors/vendor_payment_form.html', {
        'form': form,
        'vendor': vendor
    })

@login_required
def vendor_create(request):
    """
    Admin tool to add new suppliers.
    """
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save()
            messages.success(request, f"Vendor {vendor.name} added successfully.")
            return redirect('vendor_list')
    else:
        form = VendorForm()
    
    return render(request, 'vendors/vendor_form.html', {'form': form})