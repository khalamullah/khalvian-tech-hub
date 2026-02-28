from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Device
from .forms import DeviceForm
from apps.notifications.utils import send_notification


@login_required
def device_list_view(request):
    if request.user.is_admin():
        devices_list = Device.objects.all().select_related('user')
    else:
        devices_list = Device.objects.filter(
            user=request.user
        ).select_related('user')

    query = request.GET.get('q')
    if query:
        devices_list = devices_list.filter(name__icontains=query)

    status = request.GET.get('status')
    if status:
        devices_list = devices_list.filter(status=status)

    paginator = Paginator(devices_list, 10)
    page_number = request.GET.get('page')
    devices = paginator.get_page(page_number)

    return render(request, 'devices/device_list.html', {
        'devices': devices,
        'query': query,
        'status': status,
    })


@login_required
def device_detail_view(request, pk):
    if request.user.is_admin():
        device = get_object_or_404(
            Device.objects.select_related('user'), pk=pk
        )
    else:
        device = get_object_or_404(
            Device.objects.select_related('user'), pk=pk, user=request.user
        )
    return render(request, 'devices/device_detail.html', {'device': device})


@login_required
def device_create_view(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.user = request.user
            device.save()
            send_notification(
                request.user,
                f'Device "{device.name}" has been added successfully.',
                'success'
            )
            messages.success(request, 'Device added successfully.')
            return redirect('device_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = DeviceForm()
    return render(request, 'devices/device_form.html', {'form': form, 'action': 'Add'})


@login_required
def device_edit_view(request, pk):
    if request.user.is_admin():
        device = get_object_or_404(Device, pk=pk)
    else:
        device = get_object_or_404(Device, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            send_notification(
                request.user,
                f'Device "{device.name}" has been updated.',
                'info'
            )
            messages.success(request, 'Device updated successfully.')
            return redirect('device_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = DeviceForm(instance=device)
    return render(request, 'devices/device_form.html', {'form': form, 'action': 'Edit'})


@login_required
def device_delete_view(request, pk):
    if request.user.is_admin():
        device = get_object_or_404(Device, pk=pk)
    else:
        device = get_object_or_404(Device, pk=pk, user=request.user)
    if request.method == 'POST':
        device_name = device.name
        device.delete()
        send_notification(
            request.user,
            f'Device "{device_name}" has been deleted.',
            'warning'
        )
        messages.success(request, 'Device deleted successfully.')
        return redirect('device_list')
    return render(request, 'devices/device_form.html', {'device': device, 'action': 'Delete'})