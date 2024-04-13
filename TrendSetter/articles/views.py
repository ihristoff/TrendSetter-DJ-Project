from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Avg, Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core import exceptions

# Create your views here.
from django.contrib.auth import mixins as auth_mixin
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from .forms import EducationalArticleForm, CommentForm, EducationalArticleFormDelete
from .models import EducationalArticle, Comment

UserModel = get_user_model()

class EducationalArticleCreateView(auth_mixin.LoginRequiredMixin, auth_mixin.UserPassesTestMixin, views.CreateView):
    model = EducationalArticle
    form_class = EducationalArticleForm
    template_name = 'articles/article_create.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Content Creator').exists() or self.request.user.is_staff

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
        return reverse_lazy('details article', kwargs={'article_slug': self.object.slug})

class EducationalArticleUpdateView(auth_mixin.LoginRequiredMixin, auth_mixin.UserPassesTestMixin, views.UpdateView):
    model = EducationalArticle
    form_class = EducationalArticleForm
    template_name = 'articles/article_update.html'
    # success_url = reverse_lazy('article_list')
    slug_url_kwarg = "article_slug"

    def test_func(self):
        return self.request.user.is_staff
    def get_success_url(self):
        return reverse("details article", kwargs={
           "article_slug": self.object.slug,
        })


#        #Doncho 7 march workshop time 2:40 implements OwnerRequiredMixin. But some problem here

# class OwnerRequiredMixin:
#     user_field = 'user'
#     def get_object(self, queryset=None):
#         obj = super().get_object(queryset=queryset)
#         obj_user = getattr(obj, self.user_field, None)
#         if not self.request.user.is_authenticated or obj.user !=self.request.user:
#             raise exceptions.PermissionDenied
#         return obj




class EducationalArticleDetailView(auth_mixin.LoginRequiredMixin, views.DetailView):
    model = EducationalArticle
    template_name = 'articles/article_details.html'

    context_object_name = 'article'
    # comments = Comment.objects.filter(article = self.object).order_by('-date')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(article=self.object)

        # # Calculate average rating
        # average_rating = Comment.objects.filter(article=self.object).aggregate(Avg('rating'))['rating__avg']
        # context['average_rating'] = round(average_rating, 1) if average_rating else None

        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.article = self.get_object()
            new_comment.save()

            return redirect('details article', article_slug=self.get_object().slug)
        else:
            messages.error(request, 'Comment could not be added.')
            return self.get(request, *args, **kwargs)  # Render the page again with validation errors

    #Donchos way to pass the 'slug' from url
    # slug_url_kwarg = "article_slug"

    #Doncho 7 march workshop time 2:40 implements OwnerRequiredMixin


    #chatgpt learned me go override get_object method. no needed when working with pk
    def get_object(self, queryset=None):
        slug = self.kwargs.get('article_slug')
        return EducationalArticle.objects.get(slug=slug)


    # <-------increase views -------->
    def get(self, request, *args, **kwargs):
        # Call the parent class's get method to retrieve the object
        response = super().get(request, *args, **kwargs)

        # Increment the view counter
        self.object.increase_views()

        return response


# class EducationArticleListView(DetailView):
#     model = UserModel
#     template_name = 'articles/article_dashboard.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['articles'] = EducationArticle.objects.filter(user=self.object)
#         return context



class AllArticlesView(views.ListView):
    # model = EducationalArticle
    queryset = EducationalArticle.objects.all()
    template_name = 'articles/article_dashboard.html'
    context_object_name = 'articles'
    ordering = ['-created_at']  # Display articles in descending order of creation date

    paginate_by =6

    def get_queryset(self):
        return EducationalArticle.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # all_articles = EducationalArticle.objects.all().order_by('-created_at')
        # articles= context['articles']
        search_query = self.request.GET.get('q')
        filter_type = self.request.GET.get('filter')
        queryset = self.get_queryset()
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
            # Apply predefined filters
        if filter_type == 'most_viewed':
            queryset = self.get_most_viewed(queryset)
        elif filter_type == 'most_commented':
            queryset = self.get_most_commented(queryset)
        elif filter_type == 'most_recent':
            queryset = queryset.order_by('-created_at')

        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')
        context['articles'] = paginator.get_page(page)

        return context

    def get_most_viewed(self, queryset):
        return queryset.annotate(num_views=Count('views')).order_by('-num_views')
    def get_most_commented(self, queryset):
        return queryset.annotate(num_comments=Count('comment')).order_by('-num_comments')


class EducationalArticleDeleteView( auth_mixin.LoginRequiredMixin, views.DeleteView):
    model = EducationalArticle
    form_class = EducationalArticleFormDelete
    template_name = 'articles/article_delete.html'
    # success_url = reverse_lazy('article_list')
    slug_url_kwarg = "article_slug"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['image'] = self.get_object().image  # Pass the image field to the context
    #     return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object
        return kwargs

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Here we are using Django's atomic transaction to ensure integrity
        with transaction.atomic():
            # Delete the article
            self.object.delete()
            # You can also handle related objects here if needed
            # For example, if you want to keep the comments, do nothing here
            # If you want to delete the comments, do something here

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('education articles')
