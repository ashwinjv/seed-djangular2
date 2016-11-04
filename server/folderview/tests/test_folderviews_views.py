import pytest
import os
from django.conf import settings
from django.conf import urls
from django.test.utils import override_settings
from unittest import mock
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
folder_name = os.path.join(current_dir, 'fileserve')
FOLDERVIEW_FOLDERS = [folder_name]
# setattr(settings, 'FOLDERVIEW_FOLDERS', [folder_name])

@pytest.fixture
def index():
    global folder_name
    file_name = os.path.join(folder_name, 'index.html')
    os.mkdir(folder_name)
    with open(file_name, 'w') as f:
        f.write('Hello Folder View')
    yield file_name
    os.remove(file_name)
    os.rmdir(folder_name)


@pytest.fixture
def favicon():
    global folder_name, current_dir
    file_name = os.path.join(folder_name, 'favicon.ico')
    favicon_file = os.path.join(current_dir, 'tests/favicon.ico')
    os.mkdir(folder_name)
    os.system('cp {} {}'.format(favicon_file, file_name))
    yield file_name
    os.remove(file_name)
    os.rmdir(folder_name)
    

class TestViews:
    
    @mock.patch.object(settings, 'FOLDERVIEW_FOLDERS', FOLDERVIEW_FOLDERS)
    def test_can_serve_test_file(self, index, client):
        location = index.split(os.path.sep)[-1]
        folder = index.split(os.path.sep)[:-1]
        resp = client.get('/{}'.format(location))
        assert resp.status_code == 200
        assert resp.getvalue() == b'Hello Folder View'
    
    @mock.patch.object(settings, 'FOLDERVIEW_FOLDERS', FOLDERVIEW_FOLDERS)
    def test_can_serve_index_file(self, index, client):
        location = index.split(os.path.sep)[-1]
        folder = index.split(os.path.sep)[:-1]
        resp = client.get('/')
        assert resp.status_code == 200
        assert resp.getvalue() == b'Hello Folder View'
        
    @mock.patch.object(settings, 'FOLDERVIEW_FOLDERS', FOLDERVIEW_FOLDERS)
    def test_404_on_unknown_file(self, client):
        resp = client.get('/hello.test')
        assert resp.status_code == 404
        assert b'The requested URL /hello.test was not found on this server.' \
                in resp.content

    @mock.patch.object(settings, 'FOLDERVIEW_FOLDERS', [])
    def test_404_on_unknown_folder(self, index, client):
        resp = client.get('/')
        assert resp.status_code == 404
        assert b'The requested URL / was not found on this server.' \
                in resp.content

    @mock.patch.object(settings, 'FOLDERVIEW_FOLDERS', FOLDERVIEW_FOLDERS)
    def test_can_serve_favicon(self, favicon, client):
        location = favicon.split(os.path.sep)[-1]
        folder = favicon.split(os.path.sep)[:-1]
        resp = client.get('/{}'.format(location))
        assert resp.status_code == 200

    @mock.patch('mimetypes.guess_type')
    @mock.patch.object(settings, 'FOLDERVIEW_FOLDERS', FOLDERVIEW_FOLDERS)
    def test_can_serve_favicon(self, mock_guess_type, favicon, client):
        mock_guess_type.return_value = ('image/vnd.microsoft.icon', 'utf-8')
        location = favicon.split(os.path.sep)[-1]
        folder = favicon.split(os.path.sep)[:-1]
        resp = client.get('/{}'.format(location))
        assert resp.status_code == 200
        assert b'Content-Type: image/vnd.microsoft.icon' \
                in resp.serialize_headers()
        assert b'Content-Encoding: utf-8' in resp.serialize_headers()
        assert b'Content-Length: 5430' in resp.serialize_headers()


    @mock.patch('django.views.static.was_modified_since')
    @mock.patch.object(settings, 'FOLDERVIEW_FOLDERS', FOLDERVIEW_FOLDERS)
    def test_can_serve_favicon_not_modified(self, mock_mod, favicon, client):
        mock_mod.return_value = False
        location = favicon.split(os.path.sep)[-1]
        folder = favicon.split(os.path.sep)[:-1]
        resp = client.get('/{}'.format(location))
        assert resp.status_code == 304
