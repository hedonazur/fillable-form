from django.core.mail import EmailMessage
from django.conf import settings



def emailProformaClient(to_email, from_client, filepath):
    from_email = settings.EMAIL_HOST_USER
    subject = '[Office Solutions] Invoice Notification'
    body = """
    Good day,

    Please find attached invoice from {} for your immediate attention.

    regards,
    Office Solutions
    """.format(from_client)

    message = EmailMessage(subject, body, from_email, [to_email])
    message.attach_file(filepath)
    message.send()