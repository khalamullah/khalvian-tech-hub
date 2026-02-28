from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import FileResponse
import os
from .models import UploadedFile
from .forms import FileUploadForm
from apps.notifications.utils import send_notification


@login_required
def file_list_view(request):
    if request.user.is_admin():
        files_list = UploadedFile.objects.all().select_related('user')
    else:
        files_list = UploadedFile.objects.filter(
            user=request.user
        ).select_related('user')

    # Search
    query = request.GET.get('q')
    if query:
        files_list = files_list.filter(name__icontains=query)

    # Pagination
    paginator = Paginator(files_list, 10)
    page_number = request.GET.get('page')
    files = paginator.get_page(page_number)

    return render(request, 'files/file_list.html', {
        'files': files,
        'query': query,
    })


@login_required
def file_upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.name = request.FILES['file'].name
            uploaded_file.mimetype = request.FILES['file'].content_type
            uploaded_file.size = request.FILES['file'].size
            uploaded_file.save()
            send_notification(
                request.user,
                f'File "{uploaded_file.name}" uploaded successfully.',
                'success'
            )
            messages.success(request, 'File uploaded successfully.')
            return redirect('file_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = FileUploadForm()
    return render(request, 'files/file_upload.html', {'form': form})


@login_required
def file_delete_view(request, pk):
    if request.user.is_admin():
        file = get_object_or_404(UploadedFile, pk=pk)
    else:
        file = get_object_or_404(UploadedFile, pk=pk, user=request.user)
    if request.method == 'POST':
        file_name = file.name
        if os.path.isfile(file.file.path):
            os.remove(file.file.path)
        file.delete()
        send_notification(
            request.user,
            f'File "{file_name}" has been deleted.',
            'warning'
        )
        messages.success(request, 'File deleted successfully.')
        return redirect('file_list')
    return render(request, 'files/file_list.html', {'file': file})


@login_required
def file_download_view(request, pk):
    if request.user.is_admin():
        file = get_object_or_404(UploadedFile, pk=pk)
    else:
        file = get_object_or_404(UploadedFile, pk=pk, user=request.user)
    response = FileResponse(open(file.file.path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response