from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.core import exceptions

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from .forms import EducationArticleForm
from .models import EducationArticle

UserModel = get_user_model()

class EducationArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = EducationArticle
    form_class = EducationArticleForm
    template_name = 'articles/article_create.html'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article details', kwargs={'article_slug': self.object.slug})

class EducationArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EducationArticle
    form_class = EducationArticleForm
    template_name = 'articles/article_update.html'
    success_url = reverse_lazy('article_list')

    def test_func(self):
        return self.request.user.is_staff


#        #Doncho 7 march workshop time 2:40 implements OwnerRequiredMixin. But some problem here

# class OwnerRequiredMixin:
#     user_field = 'user'
#     def get_object(self, queryset=None):
#         obj = super().get_object(queryset=queryset)
#         obj_user = getattr(obj, self.user_field, None)
#         if not self.request.user.is_authenticated or obj.user !=self.request.user:
#             raise exceptions.PermissionDenied
#         return obj

#We have to  make sure that we have property 'user'   (someone may call it 'owner')
# we need to make an abstract model IHaveUser, which we inherit in our User model
# class IHaveUser(models.Model):
#     user = models.OneToOneField(
#         UserModel,
#         on_delete=models.RESTRICT,
#     )

#     class Meta:
#         abstract=True

# if we need some model to have 'user' then simply inherit instead user=ForeignKey(UserModel)


class EducationArticleDetailView(LoginRequiredMixin, DetailView):
    model = EducationArticle
    template_name = 'articles/article_details.html'

    context_object_name = 'article'

    #Donchos way to pass the 'slug' from url
    # slug_url_kwarg = "article_slug"

    #Doncho 7 march workshop time 2:40 implements OwnerRequiredMixin


    #chatgpt learned me go override get_object method. no needed when working with pk
    def get_object(self, queryset=None):
        slug = self.kwargs.get('article_slug')
        return EducationArticle.objects.get(slug=slug)

# class EducationArticleListView(DetailView):
#     model = UserModel
#     template_name = 'articles/article_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['articles'] = EducationArticle.objects.filter(user=self.object)
#         return context



class AllArticlesView(ListView):
    model = EducationArticle
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    ordering = ['-created_at']  # Display articles in descending order of creation date


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_articles = EducationArticle.objects.all().order_by('-created_at')


        search_query = self.request.GET.get('q')
        if search_query:
            context['articles'] = all_articles.filter(title__icontains=search_query)[:5]
        else:
            context['articles'] = all_articles[:5]  # Display latest 5 articles

        context['all_articles'] = all_articles
        return context

