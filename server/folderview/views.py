from django.shortcuts import render
from django.conf import settings
from django.http import Http404, HttpResponse
import os

# Create your views here.
def serve_folder_view(request, *args, **kwargs):
    file_name = kwargs.get('file_name')
    if not file_name:
        file_name = 'index.html'
    folders = getattr(settings, 'FOLDERVIEW_FOLDERS', None)
    if not folders:
        raise Http404("No folderview folders found")
    for folder in folders:
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path):
            break
    else:
        raise Http404("File {} not found in folderview".format(file_name))
    with open(file_path) as f:
        content = f.read()
    return HttpResponse(content)