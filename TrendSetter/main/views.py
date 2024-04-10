from django.shortcuts import render, redirect
from django.views import generic as views

from TrendSetter.trade_ideas.models import TradeIdea


# Create your views here.
# def index(request):
#     context = {}
#     return render(request, 'home.html', context)


class IndexView(views.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(). get_context_data(**kwargs)
        context['all_ideas'] = TradeIdea.objects.all()
        context['hide additional nav items'] = True


        return context

    #
    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect('index')
    #
    #     return super().dispatch(request, *args, **kwargs)


def custom_404(request, exception):
    return render(request, '404.html', status=404)