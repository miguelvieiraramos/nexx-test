# from django.test import TestCase
from unittest import TestCase


class TestCase(TestCase):

    def test_two_plus_two_equals_4(self):
      assert 2+2 == 4
