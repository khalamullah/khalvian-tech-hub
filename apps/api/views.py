from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from apps.devices.models import Device
from apps.notifications.models import Notification


@login_required
def api_devices(request):
    if request.user.is_admin():
        devices = Device.objects.all()
    else:
        devices = Device.objects.filter(user=request.user)
    data = [{
        'id': d.id,
        'name': d.name,
        'device_id': d.device_id,
        'status': d.status,
        'ip_address': d.ip_address,
        'last_seen': d.last_seen.isoformat() if d.last_seen else None,
    } for d in devices]
    return JsonResponse({'devices': data})


@login_required
def api_notifications(request):
    notifications = Notification.objects.filter(user=request.user)
    data = [{
        'id': n.id,
        'message': n.message,
        'type': n.notification_type,
        'is_read': n.is_read,
        'created_at': n.created_at.isoformat(),
    } for n in notifications]
    return JsonResponse({'notifications': data})


@login_required
@require_http_methods(['POST'])
def api_device_status(request, device_id):
    try:
        data = json.loads(request.body)
        device = Device.objects.get(device_id=device_id, user=request.user)
        device.status = data.get('status', device.status)
        device.save()
        return JsonResponse({'success': True, 'status': device.status})
    except Device.DoesNotExist:
        return JsonResponse({'error': 'Device not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)