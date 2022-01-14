from django.test import TestCase

# Create your tests here.
class TestFeedback(TestCase):
    def test_index(self):
        response = self.client.get('/feedback/')
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.post('/feedback/create/', {'name': 'test', 'email': 'test@gmail.com', 'text': 'test text'})
        self.assertEqual(response.status_code, 200)