import unittest

from db_connections import get_adverts_by_id, get_adverts_by_location, get_email_address, add_advertisment, keys

# tests require existance of Sherfood DB and inserting test data into tables (db.sql) 
# prior to running the tests !

class TestDBConnections(unittest.TestCase):
    def test_add_advertisment(self):
        advert_details = {'address':'Pereca, Warsaw, Poland', 'pick_up_details': 'pick up details here',
                          'expiration_date': '2027-10-10', 'glutenfree': 1, 
                          'product_name': 'product name here', 'description': 'description here'}
        coords = (52.234066, 20.996219)
        user_id = 1
        is_added = add_advertisment(advert_details, coords, user_id)
        self.assertTrue(is_added)
       
    def test_get_advert_by_location1(self):
        area = {"lat_min": 51.0, 
                "lat_max": 54.0,
                "lon_min": -3.0, 
                "lon_max": -1.0}
        results = get_adverts_by_location(area)
        result = results[0]

        self.assertEqual(result['product_name'], "Vegan Wine")
        self.assertEqual(result['address'], 'Manchester')
        self.assertEqual(result['vegan'], 1)
        self.assertEqual(result['halal'], 0)
        
        
    # 1st test needs to be passed to pass the one below:      
    def test_get_advert_added_in_1st_test(self):
        area = {"lat_min": 50.0, 
                "lat_max": 55.0,
                "lon_min": 19.0, 
                "lon_max": 22.0}
        results = get_adverts_by_location(area)
        result = results[0]

        self.assertEqual(result['description'], 'description here')
        self.assertEqual(result['address'], 'Pereca, Warsaw, Poland')
        self.assertEqual(result['vegan'], 0)
        self.assertEqual(result['glutenfree'], 1)
        
        
    def test_get_advert_by_location_no_results(self):
        area = {"lat_min": 77.0, 
        "lat_max": 78.0,
        "lon_min": 60.0, 
        "lon_max": 61.0}
        results = get_adverts_by_location(area)
        
        self.assertEqual(results, [])
        
        
    def test_get_advert_by_id(self):
        advert_id = 1
        results = get_adverts_by_id(advert_id)
        result = results[0]
        
        self.assertEqual(result['product_name'], "Vegan Wine")
        self.assertEqual(result['vegan'], 1)
        
        
    def test_get_advert_by_id_no_results(self):
        advert_id = 100
        results = get_adverts_by_id(advert_id)
        
        self.assertEqual(results, [])
        
        
    def test_get_eamil_address(self):
        item_owner_id = 1
        result = get_email_address(item_owner_id)
        
        self.assertEqual(result, 'email@email.com')
        
        
if __name__ == '__main__':
    unittest.main()
