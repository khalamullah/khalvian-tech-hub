from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def home_view(request):
    return render(request, 'core/home.html')


def about_view(request):
    return render(request, 'core/about.html')


def services_view(request):
    return render(request, 'core/services.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully. We will get back to you soon!')
            return redirect('contact')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})


def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)