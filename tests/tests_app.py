import unittest

from app import app

# tests require existance of Sherfood DB and inserting test data into tables (db.sql) 
# prior to running the tests !


class TestApp(unittest.TestCase):
    def test_connection(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        
        self.assertEqual(response.status_code, 200)
    
    
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        
        self.assertTrue(b'Welcome Back!' in response.data)
        
        
    def test_search_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/search', content_type='html/text')
        
        self.assertTrue(b'get my location' in response.data)
        
    
    def test_main_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        
        self.assertTrue(b'How to use the app' in response.data)  
    
    
    def test_sher_redirects_to_login_page(self):
        tester = app.test_client(self)
        response = tester.get('/sher', content_type='html/text')
        
        self.assertTrue(b'Welcome Back!' in response.data)  
    
        
    def test_sher_page_loads_when_logged_in(self):    
        tester = app.test_client(self)
        tester.post(
            '/login',
            data = {'username': 'test_user', 'user_password': 'password', 'signin': 1},
            follow_redirects=True)
        
        response = tester.get('/sher', content_type='html/text')
        
        self.assertTrue(b'Product name' in response.data)  
    
    
    def test_correct_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data = {'username': 'test_user', 'user_password': 'password', 'signin': 1},
            follow_redirects = True)
        
        self.assertTrue(b'logged in successfully' in response.data)
        
        
    def test_invalid_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data = {'username': 'invalid_user', 'user_password': 'invalid_password', 'signin': 1},
            follow_redirects = True)
        
        self.assertTrue(b'username or/and password are invalid' in response.data)
    
    
    def test_correct_registration(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data = {'username': 'test_user2', 'user_password': 'password2',
                    'email': 'random@email.com' ,'signup': 1},
            follow_redirects=True)
        
        self.assertTrue(b'registered successfully' in response.data)
        
        
    def test_email_already_exists(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data = {'username': 'test_user', 'user_password': 'password',
                    'email': 'email@email.com' ,'signup': 1},
            follow_redirects = True)
        
        self.assertTrue(b'email already does exist' in response.data)
        
     
    def test_logout(self):
        tester = app.test_client(self)
        tester.post(
            '/login',
            data = {'username': 'test_user', 'user_password': 'password', 'signin': 1},
            follow_redirects=True)
        
        response = tester.get('/logout',follow_redirects=True)
        
        self.assertTrue(b'Successfully logged out' in response.data)   
        
        
    def test_add_advert(self):
        tester = app.test_client(self)
        tester.post('/login',
            data = {'username': 'test_user', 'user_password': 'password', 'signin': 1},
            follow_redirects=True)
        response = tester.post('/sher/add',
            data = {'address':'Pereca, Warsaw, Poland', 'pick_up_details': 'pick up details here',
                    'expiration_date': '2027-10-10', 'glutenfree': 1, 
                    'product_name': 'product name here', 'description': 'description here'},
                    follow_redirects=True)
                
        self.assertTrue(b'successfully added' in response.data)
        
        
    def test_invalid_address(self):
        tester = app.test_client(self)
        response = tester.post(
            '/results',
            data = {'address': ''},
            follow_redirects=True)
        
        self.assertTrue(b'Invalid addres' in response.data)
    
    
    def test_results_found(self):
        tester = app.test_client(self)
        response = tester.post(
            '/results',
            data = {'address': 'Manchester'},
            follow_redirects=True)
        
        self.assertTrue(b'Vegan Wine' in response.data)
        
        
    def test_no_results_found_within_user_area(self):
        tester = app.test_client(self)
        response = tester.post(
            '/results',
            data = {'address': 'London'},
            follow_redirects=True)
        
        self.assertTrue(b'No results were found' in response.data)
        
        
    def test_get_item_details(self):
        tester = app.test_client(self)
        response = tester.post(
            '/results/item/1',
            data = {'id': '1'},
            follow_redirects=True)
        
        self.assertTrue(b'Vegan Wine' in response.data)
        
        
    def test_send_email(self):
        tester = app.test_client(self)
        response = tester.post(
            '/results/item/send',
            data = {'name': 'Kate', 'email': 'some@email.com', 'message': 'give me this item', 'userid': 1},
            follow_redirects=True)
        
        self.assertTrue(b'Message send succcessfully' in response.data)
    
    
if __name__ == '__main__':
    unittest.main()
