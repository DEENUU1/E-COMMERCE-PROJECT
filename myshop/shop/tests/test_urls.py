from django.test import TestCase


# To run this test write in a console
# coverage run manage.py test shop.tests.test_urls


# This test checks if the main page of the shop is running

class UrlTest_HomePage(TestCase):
    def testHomePage(self):
        response = self.client.get('/')
        print(response)

        self.assertEqual(response.status_code, 200)

