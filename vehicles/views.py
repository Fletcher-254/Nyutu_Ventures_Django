from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vehicle
from .forms import VehicleForm

@login_required
def vehicle_list(request):
    """Displays the main fleet table."""
    vehicles = Vehicle.objects.all().order_by('-created_at')
    return render(request, 'vehicles/vehicle_list.html', {
        'vehicles': vehicles
    })

@login_required
def vehicle_create(request):
    """Displays and processes the form to add a new vehicle."""
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle registered successfully!")
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    
    return render(request, 'vehicles/vehicle_form.html', {
        'form': form,
        'title': 'Register New Vehicle'
    })

@login_required
def vehicle_update(request, pk):
    """Displays and processes the form to update an existing vehicle."""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, f"Vehicle {vehicle.plate_number} updated.")
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    
    return render(request, 'vehicles/vehicle_form.html', {
        'form': form,
        'vehicle': vehicle,
        'title': 'Update Vehicle'
    })

@login_required
def vehicle_delete(request, pk):
    """Deletes the vehicle and returns to the list."""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    plate = vehicle.plate_number
    vehicle.delete()
    messages.warning(request, f"Vehicle {plate} removed from fleet.")
    return redirect('vehicle_list')