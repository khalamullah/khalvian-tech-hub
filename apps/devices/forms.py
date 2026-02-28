from django import forms
from .models import Device


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'device_id', 'ip_address', 'metadata']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Device Name'}),
            'device_id': forms.TextInput(attrs={'placeholder': 'Unique Device ID'}),
            'ip_address': forms.TextInput(attrs={'placeholder': '192.168.1.1'}),
            'metadata': forms.Textarea(attrs={'placeholder': '{"key": "value"}', 'rows': 4}),
        }