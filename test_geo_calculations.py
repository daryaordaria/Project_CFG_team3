from unittest import TestCase, main
import unittest

from geo_calculations import *

class TestGeoCalculations(unittest.TestCase):

    def TestLatLogViaAddress(self, extract_lat_long_via_address):
        extract_lat_long_via_address.return_value = None 
        expected = [ "lat = 52.237049, lon = 21.017532" ]
        result = extract_lat_long_via_address("Warsaw")
        self.assertEqual(expected, result)

    def TestCalDist(self, calculate_distance):
        calculate_distance.return_value = None 
        expected = 1077.5258368562315
        result = calculate_distance((48.856614, 2.3522219, 51.1078852, 17.0385376))
        self.assertEqual(expected, result)





