import pytest
import os
from django.conf import settings
from django.conf import urls
from django.test.utils import override_settings

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
folder_name = os.path.join(current_dir, 'fileserve')
file_name = os.path.join(folder_name, 'index.html')
setattr(settings, 'FOLDERVIEW_FOLDERS', [folder_name])

@pytest.fixture
def file():
    global folder_name, file_name
    os.mkdir(folder_name)
    with open(file_name, 'w') as f:
        f.write('Hello Folder View')
    yield file_name
    os.remove(file_name)
    os.rmdir(folder_name)
    
    

class TestViews:
    
    def test_can_serve_test_file(self, file, client):
        location = file.split(os.path.sep)[-1]
        folder = file.split(os.path.sep)[:-1]
        resp = client.get('/{}'.format(location))
        assert resp.status_code == 200
        assert resp.content == b'Hello Folder View'
    
    def test_can_serve_index_file(self, file, client):
        location = file.split(os.path.sep)[-1]
        folder = file.split(os.path.sep)[:-1]
        resp = client.get('/')
        assert resp.status_code == 200
        assert resp.content == b'Hello Folder View'
        
    def test_404_on_unknown_file(self, client):
        resp = client.get('/hello.test')
        assert resp.status_code == 404
        assert b'The requested URL /hello.test was not found on this server.' \
                in resp.content
        
    def test_404_on_unknown_folder(self, file, client):
        setattr(settings, 'FOLDERVIEW_FOLDERS', [])
        resp = client.get('/')
        assert resp.status_code == 404
        assert b'The requested URL / was not found on this server.' \
                in resp.content