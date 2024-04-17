from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixin
from TrendSetter.trade_ideas.forms import CreateTradeIdeaForm, DeleteTradeIdeaForm, CommentIdeaForm
from TrendSetter.trade_ideas.models import TradeIdea, Comment
from django.contrib.messages.views import SuccessMessageMixin


class CreateIdeaView(LoginRequiredMixin,  views.CreateView, SuccessMessageMixin):

    model = TradeIdea
    form_class = CreateTradeIdeaForm
    template_name = 'trade_ideas/idea_create.html'
    # success_message = 'Thank you! Your review has been updated!'

    def form_valid(self, form):
        form.instance.user = self.request.user
        symbol = form.cleaned_data.get('symbol', '')

        if 'FX:' in symbol:
            form.instance.category = 'Forex'
        elif 'COINBASE:' in symbol:
            form.instance.category = 'Crypto'
        elif 'AMEX:' in symbol or 'NASDAQ:' in symbol:
            form.instance.category = 'Stocks'
        elif 'SAXO:' in symbol:
            form.instance.category = 'Commodities'
        else:
            form.instance.category = 'Other'


        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('trade ideas dashboard')


# class TradeIdeasDashboardView(views.ListView):
#     model = TradeIdea
#     template_name = 'trade_ideas/trade_ideas_dashboard.html'
#     context_object_name = 'ideas'
#     ordering = ['-created_at']  # Display articles in descending order of creation date
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         all_ideas = TradeIdea.objects.all().order_by('-created_at')
#         search_query = self.request.GET.get('q')
#         category = request.GET.get('category')
#
#         if search_query:
#             context['ideas'] = all_ideas.filter(title__icontains=search_query)[:5]
#         else:
#             context['ideas'] = all_ideas[:6]  # Display latest 5 articles
#
#         context['all_ideas'] = all_ideas
#         return context



class TradeIdeasDashboardView(views.ListView):
    # model = EducationalArticle
    queryset = TradeIdea.objects.all()
    template_name = 'trade_ideas/trade_ideas_dashboard.html'
    context_object_name = 'ideas'
    ordering = ['-created_at']  # Display articles in descending order of creation date

    paginate_by =6

    def get_queryset(self):
        return TradeIdea.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_query = self.request.GET.get('q')
        filter_type = self.request.GET.get('filter')
        category = self.request.GET.get('category')
        symbol = self.request.GET.get('symbol')

        queryset = self.get_queryset()

            # Apply predefined filters
        if filter_type == 'most_viewed':
            queryset = self.get_most_viewed(queryset)
        elif filter_type == 'most_commented':
            queryset = self.get_most_commented(queryset)
        elif filter_type == 'most_recent':
            queryset = queryset.order_by('-created_at')
        if category:
            queryset = queryset.filter(category=category)
        if symbol:
            queryset = queryset.filter(symbol=symbol)
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)


        context['filter_type'] = filter_type
        context['category'] = category
        context['categories'] = TradeIdea.CATEGORY_CHOICES
        context['symbols'] = TradeIdea.SYMBOL_CHOICES # Dynamic categories

        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')
        context['ideas'] = paginator.get_page(page)

        return context

    def get_most_viewed(self, queryset):
        annotated_queryset = queryset.annotate(num_views=Count('views'))
        ordered_queryset = annotated_queryset.order_by('-num_views')
        print(ordered_queryset.query)
        return queryset.annotate(num_views=Count('views')).order_by('-num_views')
    def get_most_commented(self, queryset):
        return queryset.annotate(num_comments=Count('comment')).order_by('-num_comments')



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



class TradeIdeaDetailView(auth_mixin.LoginRequiredMixin, views.DetailView):
    model = TradeIdea
    template_name = 'trade_ideas/idea_details.html'
    context_object_name = 'idea'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentIdeaForm()
        context['comments'] = Comment.objects.filter(idea=self.object)
        # TODO fix the names to be with capital letters
        heatmap = self.object.category
        if heatmap == 'Indicies':
            heatmap = 'SPX500'
        elif heatmap =='Forex':
            heatmap = 'Forex'
        elif heatmap =='Crypto':
            heatmap = 'Crypto'

        context['heatmap'] = heatmap
        print(f"Heatmap value: {heatmap}")

        return context

    def post(self, request, *args, **kwargs):
        form = CommentIdeaForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.idea = self.get_object()
            new_comment.save()

            return redirect('details idea', idea_pk=self.get_object().pk)
        else:
            messages.error(request, 'Comment could not be added.')
            return self.get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        pk = self.kwargs.get('idea_pk')
        return TradeIdea.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()

        return response
