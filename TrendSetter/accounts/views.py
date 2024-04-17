from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied

from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic as views
from django.contrib.auth import views as auth_views, get_user_model, login, authenticate, logout
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import mixins as auth_mixin
from django.urls import reverse_lazy, reverse

from TrendSetter.accounts.forms import AccountUserCreationForm, ProfileForm, ChangePassword
from TrendSetter.accounts.models import Profile
from TrendSetter.articles.models import EducationalArticle, Comment
from TrendSetter.trade_ideas.models import TradeIdea

UserModel = get_user_model()

from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .models import Profile




class LoginUserView(auth_views.LoginView):
    template_name = 'accounts/login-page.html'
    success_url = reverse_lazy('index')
    # redirect_field_name = 'next'
    #default will send it to accounts/profile so we override it
    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        # Log the user in
        self.user = form.get_user()
        login(self.request, self.user)

        # Redirect to the next page
        next_page = self.request.POST.get('next', '/')
        return redirect(next_page)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '/')
        return context


class LogoutUserView(auth_views.LogoutView):
    pass
    # template_name = 'accounts/logout-page.html'
    # we do not need 'success_url'  if we are using the 'next' approach in the form on the login-page
  #  success_url = reverse_lazy('index')


class RegisterUserView(views.CreateView):
    form_class = AccountUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('index')

    #code for auto login
    def form_valid(self, form):
        # form valid will call 'save'
        result = super().form_valid(form)   #this will create our user.   super() is reference to Parent class =CreateView
        login(self.request, form.instance)   #will it work with self.object instead of self.instance

        return result


    # def from_valid(self,form):
    #     user_data = form.cleaned_data
    #     user=authenticate(
    #         username=user_data['username'],
    #         password=user_data['password1']
    #     )
    #     login(self.request, user)
    #     return super().form_valid(form)




class DetailsProfileView(auth_mixin.LoginRequiredMixin, views.DetailView):
    queryset = Profile.objects \
        .prefetch_related("user") \
        .all()
    # queryset = Profile.objects.prefetch_related().all()
    # model= Profile
    # form_class = ProfileForm
    template_name = 'accounts/details-profile.html'
    fields = ['age', 'trading_experience', 'location']


class UpdateProfileView(auth_mixin.LoginRequiredMixin, auth_mixin.UserPassesTestMixin, views.UpdateView):
    model=Profile
    form_class = ProfileForm
    # fields = ('profile_image','date_of_birth', 'age',  'trading_experience',  'location' )
    template_name = 'accounts/update-profile.html'
    pk_url_kwarg = 'pk'


    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to update this profile.")

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return get_object_or_404(Profile, pk=pk)

    def get_success_url(self):
        return reverse('profile details', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add current profile image to context
        context['profile_image'] = self.object.profile_image.url if self.object.profile_image else None

        return context

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class=form_class)
    #
    #     form.fields["date_of_birth"].widget.attrs["type"] = "date"
    #     form.fields["date_of_birth"].label = "Birthday"
    #     return form

class ChangePasswordProfileView(auth_mixin.LoginRequiredMixin, auth_views.PasswordChangeView):
    form_class = ChangePassword

    template_name = "accounts/change-password.html"
    success_url = reverse_lazy('login')


class DeleteProfileView(auth_mixin.LoginRequiredMixin, views.DeleteView):
    model=UserModel
    template_name = 'accounts/delete-profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the associated Profile object and pass it to the context
        context['profile'] = Profile.objects.get(user=self.request.user)
        # context['form'] = ProfileForm(instance=context['profile'])
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.object.user

        # Manually log out the user
        logout(request)

        # Delete the user and profile
        user.delete()
        self.object.delete()

        # Add success message
        messages.success(request, 'Your account has been deleted successfully.')

        return redirect(reverse('login'))

    def get_success_url(self):
        return reverse('index')





