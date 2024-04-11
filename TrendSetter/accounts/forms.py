from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ModelForm

from TrendSetter.accounts.models import Profile

UserModel = get_user_model()



class AccountUserCreationForm(auth_forms.UserCreationForm):

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = (UserModel.USERNAME_FIELD,)
        # fields = ('email', 'password1', 'password2')



class AccountUserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = UserModel
        fields = '__all__'



class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'



class ChangePassword(PasswordChangeForm):
    class Meta:
        model = UserModel