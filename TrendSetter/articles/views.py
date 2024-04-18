from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Avg, Count
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.core import exceptions

# Create your views here.
from django.contrib.auth import mixins as auth_mixin
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from .forms import EducationalArticleForm, CommentForm, EducationalArticleFormDelete, ArticleRatingForm, \
    EducationalArticleUpdateForm
from .models import EducationalArticle, Comment, ArticleRating


from .signals import *



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
    form_class = EducationalArticleUpdateForm
    template_name = 'articles/article_update.html'
    # success_url = reverse_lazy('article_list')
    slug_url_kwarg = "article_slug"

    def test_func(self):
        return self.request.user.groups.filter(name='Content Creator').exists() or self.request.user.is_staff
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

    template_name = 'articles/article_details.html'
    context_object_name = 'article'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(article=self.object)
        context['rating_form'] = ArticleRatingForm()


        return context

    def post(self, request, *args, **kwargs):

        form_type = request.POST.get('form_type')


        if form_type == 'comment':
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.author = request.user
                new_comment.article = self.get_object()
                new_comment.save()
                return redirect('details article', article_slug=self.get_object().slug)
            else:
                messages.error(request, 'Comment could not be added.')
                return self.get(request, *args, **kwargs)

        elif form_type == 'rating':
            rating_form = ArticleRatingForm(request.POST)
            if rating_form.is_valid():

                rating_value = rating_form.cleaned_data['rating']
                article = self.get_object()

                try:
                    rating = ArticleRating.objects.get(user=request.user, article=article)

                    # If rating exists, update it
                    rating.rating = rating_value
                    rating.save()
                except ArticleRating.DoesNotExist:
                    # If rating does not exist, create a new one
                    rating = ArticleRating.objects.create(user=request.user, article=article, rating=rating_value)

                return redirect('details article', article_slug=self.get_object().slug)

            else:
                messages.error(request, 'Rating could not be added.')
                return redirect('details article', article_slug=self.get_object().slug)
                # return JsonResponse({'success': 'Rating submitted successfully'})

    def get_object(self, queryset=None):
        slug = self.kwargs.get('article_slug')
        # return EducationalArticle.objects.get(slug=slug)

        try:
            queryset = EducationalArticle.objects.annotate(num_comments=Count('comment'))
            return queryset.get(slug=slug)
            # return EducationalArticle.objects.get(slug=slug)

        except EducationalArticle.DoesNotExist:
            raise Http404("Article does not exist")
        except EducationalArticle.user.RelatedObjectDoesNotExist:
            article = get_object_or_404(EducationalArticle, slug=slug)
            article.user = None
            return article

    def get(self, request, *args, **kwargs):
        # Call the parent class's get method to retrieve the object
        response = super().get(request, *args, **kwargs)
        # Increment the view counter
        self.object.increase_views()
        return response


class AllArticlesView(views.ListView):

    queryset = EducationalArticle.objects.all()
    template_name = 'articles/article_dashboard.html'
    context_object_name = 'articles'
    # ordering = ['-created_at']
    paginate_by =6

    def get_queryset(self):
        return EducationalArticle.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset().annotate(avg_rating=Avg('articlerating__rating'), num_comments=Count('comment'),  )
        category = self.request.GET.get('category')
        search_query = self.request.GET.get('q')
        filter_type = self.request.GET.get('filter')

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
            # Apply predefined filters
        if category:
            queryset = queryset.filter(category=category)

        if filter_type == 'most_viewed':
            queryset = self.get_most_viewed(queryset)
        elif filter_type == 'highest_rated':
            queryset = queryset.annotate(avg_rating=Avg('articlerating__rating')).order_by('-avg_rating')
        elif filter_type == 'most_commented':
            queryset = self.get_most_commented(queryset)
        elif filter_type == 'most_recent':
            queryset = queryset.order_by('-created_at')

        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')
        context['articles'] = paginator.get_page(page)
        context['category'] = category
        context['categories'] = EducationalArticle.CATEGORY_CHOICES

        return context

    def get_most_viewed(self, queryset):
        return queryset.annotate(num_views=Count('views')).order_by('-num_views')
    def get_most_commented(self, queryset):
        return queryset.annotate(num_comments=Count('article_comments')).order_by('-num_comments')


class EducationalArticleDeleteView( auth_mixin.LoginRequiredMixin, auth_mixin.UserPassesTestMixin, views.DeleteView):
    model = EducationalArticle
    form_class = EducationalArticleFormDelete
    template_name = 'articles/article_delete.html'
    slug_url_kwarg = "article_slug"

    def test_func(self):
        return self.request.user.groups.filter(name='Content Creator').exists() or self.request.user.is_staff

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object
        return kwargs

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        with transaction.atomic():

            self.object.delete()


        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('education articles')
