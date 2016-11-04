class TestViews:
    def test_get_hello(self, client):
        resp = client.get('/api/v1/')
        assert resp.status_code == 200, \
            'Should be able to access /api/v1/'
        assert resp.content == b'Hello from server'