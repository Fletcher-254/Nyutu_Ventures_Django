import os
import django

# 1. Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_test_accounts():
    print("🚀 Starting Test Account Creation...")

    # Define our 3 Personas
    personas = [
        {
            "email": "director@nyutu.com",
            "password": "pass_director_123",
            "role": "Director",
            "first_name": "Executive",
            "last_name": "Director"
        },
        {
            "email": "pm@nyutu.com",
            "password": "pass_manager_123",
            "role": "Manager",
            "first_name": "Project",
            "last_name": "Manager"
        },
        {
            "email": "admin@nyutu.com",
            "password": "pass_admin_123",
            "role": "Admin",
            "first_name": "System",
            "last_name": "Admin"
        }
    ]

    for data in personas:
        # Check if user already exists to avoid duplicates
        user, created = User.objects.get_or_create(email=data['email'])
        
        if created:
            user.set_password(data['password'])
            user.role = data['role']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            # Make them all staff so they can access the backend if needed
            user.is_staff = True 
            user.save()
            print(f"✅ Created: {data['role']} ({data['email']})")
        else:
            print(f"🟡 Skipped: {data['email']} already exists.")

    print("\n🎉 Test accounts are ready for development!")

if __name__ == "__main__":
    create_test_accounts()