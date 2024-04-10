from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic as views
from django.contrib.auth import views as auth_views, get_user_model, login, authenticate, logout
from django.contrib.auth import forms as auth_forms

from django.urls import reverse_lazy, reverse

from TrendSetter.accounts.forms import AccountUserCreationForm, ProfileForm
from TrendSetter.accounts.models import Profile
from TrendSetter.articles.models import EducationalArticle, Comment
from TrendSetter.trade_ideas.models import TradeIdea

UserModel = get_user_model()

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




class DetailsProfileView(LoginRequiredMixin, views.DetailView):
    queryset = Profile.objects \
        .prefetch_related("user") \
        .all()
    # queryset = Profile.objects.prefetch_related().all()
    # model= Profile
    # form_class = ProfileForm
    template_name = 'accounts/details-profile.html'
    fields = ['age', 'trading_experience', 'location']


class UpdateProfileView(LoginRequiredMixin, views.UpdateView):
    queryset = Profile.objects.all()

    fields = ('profile_image','date_of_birth', 'age',  'trading_experience',  'location' )
    template_name = 'accounts/update-profile.html'

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

class ChangePasswordProfileView(LoginRequiredMixin, auth_views.PasswordChangeView):
    pass


class DeleteProfileView(LoginRequiredMixin, views.DeleteView):
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
