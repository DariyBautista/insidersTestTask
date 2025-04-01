from django.core.mail import send_mail
from django.conf import settings 

def generate_random_password(length=8):
    import random
    import string
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def send_password_reset_email(user, new_password):
    send_mail(
        'Your new password',
        f'Your new password is: {new_password}',
        settings.EMAIL_HOST_USER,  
        [user.email],
        fail_silently=False,
    )
