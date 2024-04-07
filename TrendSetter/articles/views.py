from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render
from django.core import exceptions

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from .forms import EducationalArticleForm
from .models import EducationalArticle

UserModel = get_user_model()

class EducationalArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = EducationalArticle
    form_class = EducationalArticleForm
    template_name = 'articles/article_create.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["title"].widget.attrs["placeholder"] = "Title"
        form.fields["description"].widget.attrs["placeholder"] = "Description"
        form.fields["image"].widget.attrs["placeholder"] = "Upload Image"

        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article details', kwargs={'article_slug': self.object.slug})

class EducationalArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EducationalArticle
    form_class = EducationalArticleForm
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


class EducationalArticleDetailView(LoginRequiredMixin, DetailView):
    model = EducationalArticle
    template_name = 'articles/article_details.html'

    context_object_name = 'article'

    #Donchos way to pass the 'slug' from url
    # slug_url_kwarg = "article_slug"

    #Doncho 7 march workshop time 2:40 implements OwnerRequiredMixin


    #chatgpt learned me go override get_object method. no needed when working with pk
    def get_object(self, queryset=None):
        slug = self.kwargs.get('article_slug')
        return EducationalArticle.objects.get(slug=slug)

# class EducationArticleListView(DetailView):
#     model = UserModel
#     template_name = 'articles/article_dashboard.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['articles'] = EducationArticle.objects.filter(user=self.object)
#         return context



class AllArticlesView(ListView):
    # model = EducationArticle
    queryset = EducationalArticle.objects.all()
    template_name = 'articles/article_dashboard.html'
    context_object_name = 'articles'
    ordering = ['-created_at']  # Display articles in descending order of creation date

    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_articles = EducationalArticle.objects.all().order_by('-created_at')
        # articles= context['articles']

        search_query = self.request.GET.get('q')
        if search_query:
            context['articles'] = all_articles.filter(title__icontains=search_query)
        else:
            context['articles'] = all_articles

        paginator = Paginator(context['articles'], self.paginate_by)
        page = self.request.GET.get('page')
        context['articles'] = paginator.get_page(page)

        # context['all_articles'] = all_articles
        return context


