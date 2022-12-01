import unittest

from geo_calculations import calculate_distance, extract_lat_long_via_address


class TestGeoCalculations(unittest.TestCase):
    def test_extracting_coords_from_address(self):
        # coords taken from https://www.findlatitudeandlongitude.com/l/ul.+Pereca+2%2C+00-849+Warsaw%2C+Poland/3050857/:
        expected = (round(52.234066, 2), round(20.996219, 2))
        lat, lon = extract_lat_long_via_address("Pereca 2, Warszawa")
        result = (round(lat, 2), round(lon, 2))
        self.assertEqual(expected, result)
        
    def test_area_lat(self):
        # check whether the distance between max and min latitude is in fact 20km, which should be approximately 0.18 degree
        area = calculate_distance((52.234066,20.996219))
        diff_in_degrees = round(area['lat_max'] - area['lat_min'],2)
        twenty_km_in_degrees = 0.18
        self.assertEqual(diff_in_degrees, twenty_km_in_degrees)
        
    def test_is__within_area(self):
        # check whether a point is within 10km area
        coords1 = extract_lat_long_via_address("Pereca 2, Warszawa")
        coords_close = extract_lat_long_via_address("Pereca 3, Warszawa")
        coords_far = extract_lat_long_via_address("London")
        area = calculate_distance(coords1)

        self.assertTrue(area['lat_max'] >= coords_close[0] >= area['lat_min'])
        self.assertTrue(area['lon_max'] >= coords_close[1] >= area['lon_min'])
        self.assertFalse(area['lat_max'] >= coords_far[1] >= area['lat_min'])
        self.assertFalse(area['lon_max'] >= coords_far[1] >= area['lon_min'])
        
        
if __name__ == '__main__':
    unittest.main()
