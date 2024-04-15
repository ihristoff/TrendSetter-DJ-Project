from django.shortcuts import render, redirect
from django.views import generic as views
from TrendSetter.accounts.models import TrendSetterUser
from TrendSetter.articles.models import EducationalArticle
from TrendSetter.trade_ideas.models import TradeIdea


from django.utils import timezone
from django.contrib.sessions.models import Session

class IndexView(views.TemplateView):
    template_name = 'common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ideas_count'] = TradeIdea.objects.all().count()
        context['articles_count'] = EducationalArticle.objects.all().count()
        context['users_count'] = TrendSetterUser.objects.all().count()
        content_creators_count = TrendSetterUser.objects.filter(groups__name='Content Creator').count()
        staff_count = TrendSetterUser.objects.filter(is_staff=True).count()
        total_creators_count = content_creators_count + staff_count
        context['content_creators_count'] = total_creators_count

        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())

        # Get user ids from active sessions
        user_ids = [s.get_decoded().get('_auth_user_id') for s in active_sessions]

        # Query online users
        online_users = TrendSetterUser.objects.filter(id__in=user_ids)

        # Count online users
        online_users_count = online_users.count()

        # Add online_users_count to the context
        context['online_users_count'] = online_users_count

        return context


def about(request):
    return render(request, 'common/about.html')


def faq(request):
    return render(request, 'common/faq.html')


def contact(request):
    return render(request, 'common/contact.html')


def terms_and_conditions(request):
    return render(request, 'common/terms_and_conditions.html')


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_403(request, exception):
    return render(request, '403.html', status=403)
