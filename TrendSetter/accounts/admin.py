from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth import admin as auth_admin

from TrendSetter.accounts.forms import AccountUserChangeForm
from TrendSetter.accounts.models import TrendSetterUser
from TrendSetter.accounts.views import AccountUserCreationForm

UserModel = get_user_model()

@admin.register(UserModel)
#using auth_admin.UserAdmin requires  'form' 'add_form' 'fieldsets' 'add_fieldsets'
class TrendSetterUserAdmin(auth_admin.UserAdmin):

    list_display = ('email','is_superuser','is_staff','last_login')
    list_filter = ('is_staff','last_login')
    ordering = ('email','is_staff')
    search_fields = ('email',)

    form = AccountUserChangeForm
    fieldsets = (
        (None, {'fields': ('email','password')}),
        ('Permissions', {'fields': ('is_superuser','is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_form = AccountUserCreationForm
    add_fieldsets = (
        (None,
         {
             'classes': ('wide',),
             'fields': ('email', 'password1','password2'),
          },
         ),
    )



