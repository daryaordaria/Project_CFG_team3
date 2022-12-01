import unittest

from email_sender import render_email_msg
from config import EMAIL_USER

# tests require existance of Sherfood DB and inserting test data into tables (db.sql) 
# prior to running the tests !

class TestEmail(unittest.TestCase):
    def test_render_email_message(self):
        contact_form = {'name': 'random_name',
                        'email': 'someemail@someemail.com',
                        'message': 'hello world',
                        'userid': 1}
        owner_user_email = 'email@email.com'
        result = render_email_msg(contact_form)
        msg, is_rendered = result
        expected_msg = f"""From: {EMAIL_USER}
                            To: {owner_user_email}
                            Subject: Sherfood Announcement response


                            Please contact the user that is interested in your announcement. Their details are as follows:
                            Name: {contact_form['name']}
                            Email address: {contact_form['email']}
                            Messsage:
                            {contact_form['message']}
                            
                            Kind regards,
                            Sherfood.
                            """
        
        self.assertEqual(msg.body, expected_msg)
        self.assertEqual(is_rendered, True)
        
        
if __name__ == '__main__':
    unittest.main()
