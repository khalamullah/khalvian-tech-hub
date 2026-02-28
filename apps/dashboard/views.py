from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.models import User
from apps.devices.models import Device
from apps.files.models import UploadedFile
from apps.blog.models import Post
from apps.core.models import ContactMessage
from apps.notifications.models import Notification


@login_required
def dashboard_view(request):
    if request.user.is_admin():
        return redirect('admin_dashboard')
    devices = Device.objects.filter(
        user=request.user
    ).select_related('user')
    files = UploadedFile.objects.filter(
        user=request.user
    ).select_related('user')
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).select_related('user')
    return render(request, 'dashboard/user_dashboard.html', {
        'devices': devices,
        'files': files,
        'notifications': notifications,
        'device_count': devices.count(),
        'file_count': files.count(),
        'notification_count': notifications.count(),
    })


@login_required
def admin_dashboard_view(request):
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    users = User.objects.all()
    devices = Device.objects.all().select_related('user')
    files = UploadedFile.objects.all().select_related('user')
    posts = Post.objects.all().select_related('author', 'category')
    messages_count = ContactMessage.objects.filter(is_read=False).count()
    return render(request, 'dashboard/admin_dashboard.html', {
        'user_count': users.count(),
        'device_count': devices.count(),
        'file_count': files.count(),
        'post_count': posts.count(),
        'messages_count': messages_count,
        'recent_users': users.order_by('-date_joined')[:5],
        'recent_devices': devices.order_by('-created_at')[:5],
    })


@login_required
def admin_users_view(request):
    if not request.user.is_admin():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/admin_users.html', {'users': users})


@login_required
def admin_devices_view(request):
    if not request.user.is_admin():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    devices = Device.objects.all().select_related('user').order_by('-created_at')
    return render(request, 'dashboard/admin_devices.html', {'devices': devices})


@login_required
def admin_messages_view(request):
    if not request.user.is_admin():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    contact_messages = ContactMessage.objects.all().order_by('-submitted_at')
    contact_messages.filter(is_read=False).update(is_read=True)
    return render(request, 'dashboard/admin_messages.html', {'contact_messages': contact_messages})