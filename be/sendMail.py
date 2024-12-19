import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

def send_mail(item_name, item_price, to_email):
    sg = sendgrid.SendGridAPIClient(api_key='sendgrid api key')
    from_email = Email("example@mail.com")  # Change to your verified sender
    to_email = To(to_email)  # Change to your recipient
    subject = "An item you have favuorited is now cheaper!"
    content = Content("text/plain", "Item: "+ item_name + "\nPrice is now: " + item_price)
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)