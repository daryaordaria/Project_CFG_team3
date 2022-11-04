from flask import Flask, flash, render_template, request
import re
from connect_database_email import get_email_address
from login_email import EMAIL_USER,EMAIL_PASSWORD
from flask_mail import Message,Mail

mail = Mail()

app = Flask(__name__)
app.secret_key = 'I#love<3cookies'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = EMAIL_USER
app.config["MAIL_PASSWORD"] = EMAIL_PASSWORD

mail.init_app(app)


@app.route('/results/item/<userid>',methods =['GET','POST'])
def contact_form(userid):

   if request.method == 'POST':
     name = request.form['name']
     email_address = request.form['contact']
     message = request.form['message']
     if not name or message or email_address:
        flash('This field is required. Please try again.')
     elif not re.search('@', email_address):
         flash('This is not a valid email address please try again.')
     else:
        result = get_email_address(userid)
        msg = Message(subject='Announcement response',sender=EMAIL_USER,recipients=result)
        msg.body = """From: %s
                     To: %s
                     Subject: Announcement response


                     Please contact the user that is interested in your announcement. Their details are as follows.
                     Name: %s
                     Email address: %s
                     
                     Kind regards,
                     Sherfood.
                    """ % (EMAIL_USER, result, name, email_address)
        mail.send(msg)
        flash('Your email was sent successfully')

        return render_template('item.html')

   else:
    return render_template('item.html')

if __name__ == '__main__' :
    app.run(debug=True)





