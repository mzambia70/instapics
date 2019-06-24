from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_welcome_email(name, receiver):
    #Creating message subject and sender
    subject = 'Instagram Account creation successful'
    sender = 'mzambia70@gmail.com'

    #passing in the context variables
    text_context = render_to_string('email/newsemail.txt', {"name":name})
    html_content = render_to_string('email/newsemail.html',{"name":name})

    msg = EmailMultiAlternatives(subject, text_context, sender, [receiver])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()