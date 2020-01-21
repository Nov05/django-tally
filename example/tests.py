# example/tests.py
from django.test import TestCase


# Create your tests here.
'''
https://docs.djangoproject.com/en/3.0/topics/testing/overview/
When you run your tests, the default behavior of the test utility 
is to find all the test cases (that is, subclasses of unittest.TestCase) 
in any file whose name begins with test, automatically build a test suite 
out of those test cases, and run that suite.
'''

#######################################################
# test exmaple - bucket list
#######################################################
from .models import ExampleBucketlist

class ModelTestCase(TestCase):
    """This class defines the test suite for the bucketlist model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.bucketlist_name = "Write world class code"
        self.bucketlist = ExampleBucketlist(name=self.bucketlist_name)

    def test_model_can_create_a_bucketlist(self):
        """Test the bucketlist model can create a bucketlist."""
        old_count = ExampleBucketlist.objects.count()
        self.bucketlist.save()
        new_count = ExampleBucketlist.objects.count()
        self.assertNotEqual(old_count, new_count)


#######################################################
# test exmaple - REST framework
#######################################################
from rest_framework.test import APIClient
from rest_framework import status
# from django.core.urlresolvers import reverse # removed since Django 2.0
from django.urls import reverse


# Define this after the ModelTestCase
class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.bucketlist_data = {'name': 'Unit test 001'}
        self.response = self.client.post(
            reverse('create'),
            self.bucketlist_data,
            format="json")

    def test_api_can_create_a_bucketlist(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_bucketlist(self):
        """Test the api can get a given bucketlist."""
        bucketlist = ExampleBucketlist.objects.get()
        response = self.client.get(
            reverse('details',
            kwargs={'pk': bucketlist.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, bucketlist)

    def test_api_can_update_bucketlist(self):
        """Test the api can update a given bucketlist."""
        # bucketlist = ExampleBucketlist.objects.get()
        change_bucketlist = {'name': 'Something new'}
        res = self.client.put(
            reverse('details', kwargs={'pk': bucketlist.id}),
            change_bucketlist, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_bucketlist(self):
        """Test the api can delete a bucketlist."""
        # bucketlist = ExampleBucketlist.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': bucketlist.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)