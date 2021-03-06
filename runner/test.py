from django.test import TestCase
from runner.models import Portfolio

class AnimalTestCase(TestCase):
    def setUp(self):
        Portfolio.objects.create(url="/assts/img.jpg")
        Portfolio.objects.create(url="/assts/img2.jpg")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Portfolio.objects.get(pk=1)

        self.assertEqual(lion.url, '/assts/img.jpg')

