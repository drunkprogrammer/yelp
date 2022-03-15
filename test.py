import unittest

from user_rating_behavior import calculate_user_rating_behavior

class TestCalculate(unittest.TestCase):
    def test_calculate_user_rating_behavior(self):
        """
        test that it can calculate the casual user rating behavior
        """
        file = ""
        result = calculate_user_rating_behavior(file)