from django.test import TestCase

# Create your tests here.
class HelloWorldTestCase(TestCase):
    def setUp(self):
        # We usually create objects of the models here
        pass

    def test_hello(self):
        resp = self.client.get('')
        self.assertEqual(resp.data, {
                "message": "Howdy! Thanks for visiting the back-end of Privilege Walk"
            })