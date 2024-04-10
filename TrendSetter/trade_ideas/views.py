from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from TrendSetter.trade_ideas.forms import CreateTradeIdeaForm, DeleteTradeIdeaForm
from TrendSetter.trade_ideas.models import TradeIdea

from django.contrib.messages.views import SuccessMessageMixin


class CreateIdeaView(LoginRequiredMixin,  views.CreateView, SuccessMessageMixin):

    model = TradeIdea
    form_class = CreateTradeIdeaForm
    template_name = 'trade_ideas/idea_create.html'
    success_message = 'Thank you! Your review has been updated!'

    # def test_func(self):
    #     return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')



class TradeIdeasDashboardView(views.ListView):
    model = TradeIdea
    template_name = 'trade_ideas/trade_ideas_dashboard.html'
    context_object_name = 'ideas'
    ordering = ['-created_at']  # Display articles in descending order of creation date


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_ideas = TradeIdea.objects.all().order_by('-created_at')
        search_query = self.request.GET.get('q')
        if search_query:
            context['ideas'] = all_ideas.filter(title__icontains=search_query)[:5]
        else:
            context['ideas'] = all_ideas[:6]  # Display latest 5 articles

        context['all_ideas'] = all_ideas
        return context


class DeleteTradeIdeaView(views.DeleteView):
    model = TradeIdea
    form_class = DeleteTradeIdeaForm
    template_name = 'trade_ideas/delete_idea.html'

    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form_class(instance=self.object)
        context['form'] = form
        return context


