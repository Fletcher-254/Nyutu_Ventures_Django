from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vehicle
from .forms import VehicleForm

def is_admin(user):
    return user.role.lower() == 'admin'

@login_required
def vehicle_list(request):
    """Accessible by Admin, Director, and Manager."""
    vehicles = Vehicle.objects.all().order_by('-created_at')
    
    # Stats for the top header cards
    total_count = vehicles.count()
    # If your model has a status field, use it; otherwise, default to total
    active_count = vehicles.filter(status='Active').count() if hasattr(Vehicle, 'status') else total_count

    return render(request, 'vehicles/vehicle_list.html', {
        'vehicles': vehicles,
        'total_count': total_count,
        'active_count': active_count
    })

@login_required
def vehicle_create(request):
    if not is_admin(request.user):
        messages.error(request, "Only Admins can register new vehicles.")
        return redirect('vehicle_list')

    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle registered successfully!")
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    
    return render(request, 'vehicles/vehicle_form.html', {'form': form, 'title': 'Register New'})

@login_required
def vehicle_update(request, pk):
    if not is_admin(request.user):
        messages.error(request, "Only Admins can edit vehicle details.")
        return redirect('vehicle_list')

    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, f"Vehicle {vehicle.plate_number} updated.")
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    
    return render(request, 'vehicles/vehicle_form.html', {'form': form, 'vehicle': vehicle})

@login_required
def vehicle_delete(request, pk):
    if not is_admin(request.user):
        messages.error(request, "Only Admins can delete vehicles.")
        return redirect('vehicle_list')

    vehicle = get_object_or_404(Vehicle, pk=pk)
    plate = vehicle.plate_number
    vehicle.delete()
    messages.warning(request, f"Vehicle {plate} removed.")
    return redirect('vehicle_list')