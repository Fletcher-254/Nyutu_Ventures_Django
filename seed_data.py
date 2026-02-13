import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from employees.models import Employee
from vendors.models import Vendor

def seed():
    print("Seeding dummy data for testing...")
    
    # 1. Create Dummy Employees
    employees = [
        {"first_name": "James", "last_name": "Mwangi", "designation": "Driver"},
        {"first_name": "Sarah", "last_name": "Achieng", "designation": "Operations"},
        {"first_name": "Peter", "last_name": "Kiprono", "designation": "Mechanic"},
    ]
    for emp in employees:
        Employee.objects.get_or_create(**emp)

    # 2. Create Dummy Vendors
    vendors = ["Shell Kenya", "Toyota Service", "TotalEnergies"]
    for v in vendors:
        Vendor.objects.get_or_create(name=v)

    print("Successfully seeded! To clear this later, tell the client to run: Employee.objects.all().delete()")

if __name__ == "__main__":
    seed()