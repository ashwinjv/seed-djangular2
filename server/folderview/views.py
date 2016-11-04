from django.shortcuts import render
from django.conf import settings
from django.http import (
                Http404, HttpResponse, HttpResponseNotModified,
                FileResponse
                )
from django.utils.http import http_date
from django.views import static
import mimetypes
import stat
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
        fullpath = os.path.join(folder, file_name)
        if os.path.isfile(fullpath):
            break
    else:
        raise Http404("File {} not found in folderview".format(file_name))
    # Respect the If-Modified-Since header.
    statobj = os.stat(fullpath)
    if not static.was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj.st_mtime, statobj.st_size):
        return HttpResponseNotModified()
    content_type, encoding = mimetypes.guess_type(fullpath)
    content_type = content_type or 'application/octet-stream'
    response = FileResponse(open(fullpath, 'rb'), content_type=content_type)
    response["Last-Modified"] = http_date(statobj.st_mtime)
    if stat.S_ISREG(statobj.st_mode):
        response["Content-Length"] = statobj.st_size
    if encoding:
        response["Content-Encoding"] = encoding
    return response