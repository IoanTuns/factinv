from django.urls import reverse_lazy, reverse
from django.template.loader import get_template
from factinv.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives, EmailMessage
from core.views.views import logo_email

def register_email(message):
    """
    TODO: Email validation verification

    This function get messege parateters
    and send activation email with txt and html template
    """
    register_email_plaintext = get_template('email/user_activations_msg.txt')
    register_email_htmly     = get_template('email/user_activations_msg.html')
    kwargs = {
        "uidb64": message['uid'],
        "token": message['token']
    }
    activation_url = reverse("accounts:activate", kwargs=kwargs )
    activate_url = "{0}://{1}{2}".format(message['scheme'], message['current_site'], activation_url)
    # sender =('Confirmare cont <'+EMAIL_HOST_USER+'>')
    sender =('Confirmare cont FactInv')
    from_email = EMAIL_HOST_USER
    username = message['user']
    subject, from_email, to = message['mail_subject'], from_email, message['email_to']
    text_content = register_email_plaintext.render({ 'username': username, 'activate_url': activate_url })
    html_content = register_email_htmly.render({ 'username': username, 'activate_url': activate_url })
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    # from https://samoylov.eu/2016/10/19/sending-html-emails-with-embedded-images-from-django/
    # msg.content_subtype = 'html'  # Main content is text/html
    msg.mixed_subtype = 'related'  # This is critical, otherwise images will be displayed as attachments!
    email_logo = logo_email()
    msg.attach(email_logo)
    msg.send() 
    