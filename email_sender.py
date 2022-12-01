import re
from flask_mail import Message
from db_connections import get_email_address
from config import EMAIL_USER



def render_email_msg(contact_form):
    name = contact_form['name']
    email_address = contact_form['email'].strip()
    message = contact_form['message']
    item_owner_id = contact_form['userid']
    
    if not (name or message or email_address):
        flash_msg = 'All the fields are required. Please try again.'
    elif not re.match('^.*@.*\..*$', email_address):
        flash_msg = 'This is not a valid email address. Please try again.'
    else:
        recipient_email = get_email_address(item_owner_id)
        if not recipient_email:
            flash_msg = 'An error occurred whilst connecting to the DB. Please try again'
        else:
            try:
                msg = Message(subject='Sherfood response',sender=EMAIL_USER,recipients=[recipient_email])
                msg.body = """From: %s
                            To: %s
                            Subject: Sherfood Announcement response


                            Please contact the user that is interested in your announcement. Their details are as follows:
                            Name: %s
                            Email address: %s
                            Messsage:
                            %s
                            
                            Kind regards,
                            Sherfood.
                            """ % (EMAIL_USER, recipient_email, name, email_address, message)
                return msg, True
            except:
                flash_msg = 'We were not able to send the email. Try again later'
            
    return flash_msg, False