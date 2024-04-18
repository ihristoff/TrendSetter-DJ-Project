from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth import admin as auth_admin

from TrendSetter.accounts.forms import AccountUserChangeForm
from TrendSetter.accounts.models import TrendSetterUser, Profile
from TrendSetter.accounts.views import AccountUserCreationForm

UserModel = get_user_model()


@admin.register(UserModel)
# using auth_admin.UserAdmin requires  'form' 'add_form' 'fieldsets' 'add_fieldsets'
class TrendSetterUserAdmin(auth_admin.UserAdmin):
    list_display = ('email', 'is_superuser', 'is_staff', 'last_login', 'date_joined')
    list_filter = ('is_staff', 'last_login', 'date_joined')
    ordering = ('email', 'is_staff')
    search_fields = ('email',)

    form = AccountUserChangeForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_form = AccountUserCreationForm
    add_fieldsets = (
        (None,
         {
             'classes': ('wide',),
             'fields': ('email', 'password1', 'password2'),
         },
         ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'trading_experience', 'send_mail_for_new_article', 'show_email')
    list_filter = ('trading_experience', 'send_mail_for_new_article', 'show_email')
    search_fields = ('user__email', 'username')
