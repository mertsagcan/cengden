import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

def send_mail(item_name, item_price, to_email):
    sg = sendgrid.SendGridAPIClient(api_key='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')
    from_email = Email("e2310449@ceng.metu.edu.tr")  # Change to your verified sender
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