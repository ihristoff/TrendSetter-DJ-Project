from mailjet_rest import Client
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

User = get_user_model()

def send_welcome_email(user):
    mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY), version='v3.1')

    user_email = user


    html_content = render_to_string('accounts/welcome_email.html', {'username': user})

    data = {
        'Messages': [
            {
                'From': {
                    'Email': settings.DEFAULT_FROM_EMAIL  # Make sure this is a verified email in Mailjet
                },
                'To': [
                    {
                        'Email': user_email
                    }
                ],
                'Subject': 'Welcome to TrendSetter!',
                'TextPart': f'Welcome to Trendsetter, {user_email}!',
                'HTMLPart': html_content
            }
        ]
    }

    result = mailjet.send.create(data=data)

    if result.status_code == 200:
        print(f'Welcome email sent to {user_email}')
    else:
        print(f'Failed to send welcome email to {user_email}. Error: {result.json()}')