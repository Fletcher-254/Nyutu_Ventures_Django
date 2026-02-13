from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Expense
from vendors.models import VendorAccount

@receiver(post_save, sender=Expense)
def update_vendor_balance_on_expense(sender, instance, created, **kwargs):
    """
    When an expense is saved and linked to a vendor, 
    increase the vendor's total_owed.
    """
    if created and instance.related_vendor:
        # Get or create account in case it doesn't exist
        account, _ = VendorAccount.objects.get_or_create(vendor=instance.related_vendor)
        account.total_owed += instance.amount
        account.save()