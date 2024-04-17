from django.contrib.auth import get_user_model
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import PasswordChangeForm

from django import forms
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


# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = '__all__'


class ChangePassword(PasswordChangeForm):
    class Meta:
        model = UserModel



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_image',
            'username',
            'bio',
            'date_of_birth',
            'age',
            'location',
            'trading_experience',
            'send_mail_for_new_article',
        ]
        labels = {
            'profile_image': 'Profile Image',
            'username': 'Username*',
            'bio':'Tell us something about yourself',
            'send_mail_for_new_article': 'Send Mail for New Article',
            'date_of_birth': 'Date of Birth',
            'age': 'Age',
            'location': 'Location',
            'trading_experience': 'Trading Experience',
        }
        placeholders = {
            'username': 'Enter your username',
            'date_of_birth': 'YYYY-MM-DD',
            'age': 'Enter your age',
            'location': 'Enter your location',
        }
        help_texts = {
            'send_mail_for_new_article': 'Receive email notifications for new articles',
            'bio': 'Information is public',
            'date_of_birth': 'Enter your date of birth in YYYY-MM-DD format',
            'trading_experience': 'Select your trading experience level',
        }
        error_messages = {
            'username': {
                'unique': 'This username is already taken.',
            },
        }



    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # self.fields['bio'].widget.attrs.update({
        #     'rows': 2,
        # })



        for field in self.fields:
            placeholder = self.Meta.placeholders.get(field, '')
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholder,
            })


        # Set the initial value for the profile_image field
        if self.instance.profile_image:
            self.fields['profile_image'].widget.attrs['current_image'] = self.instance.profile_image.url