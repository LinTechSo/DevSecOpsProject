#!/bin/python3
import app, unittest
class TestHello(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_status1(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status, '200 OK')

    def test_status2(self):
        rv = self.app.get('/login')
        self.assertEqual(rv.status, '200 OK')

    def test_ok_response(self):
        rv = self.app.get('/v1/ok')
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(rv.data, b'{\n  "message": "ok"\n}\n')

if __name__ == '__main__':
    import xmlrunner
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    unittest.main(testRunner=runner)
    unittest.main()