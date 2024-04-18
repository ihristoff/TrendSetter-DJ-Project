from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from mailjet_rest import Client

from .models import EducationalArticle
from ..accounts.models import Profile

from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=EducationalArticle)
def send_new_article_email(sender, instance, **kwargs):
    if kwargs.get('created', False):
        users_to_notify = User.objects.filter(profile__send_mail_for_new_article=True)
        article_link = f"http://your_domain.com/articles/article/{instance.slug}/"

        mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY), version='v3.1')

        for user in users_to_notify:
            subject = 'New Article Notification'
            message = f'A new article "{instance.title}" has been published. Check it out at {article_link}.'
            # html_content = render_to_string('articles/email_notification.html', {'article_title': instance.title, 'article_link': article_link})

            data = {
                'Messages': [
                    {
                        'From': {
                            'Email': settings.DEFAULT_FROM_EMAIL  # Make sure this is a verified email in Mailjet
                        },
                        'To': [
                            {
                                'Email': user.email
                            }
                        ],
                        'Subject': subject,
                        'TextPart': message,
                        # 'HTMLPart': html_content
                    }
                ]
            }

            result = mailjet.send.create(data=data)

            if result.status_code != 200:
                print(f'Failed to send email to {user.email}. Error: {result.json()}')