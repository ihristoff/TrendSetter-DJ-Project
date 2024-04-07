from django.urls import path

from TrendSetter.accounts.views import LoginUserView, RegisterUserView, LogoutUserView, DetailsProfileView, \
    UpdateProfileView, DeleteProfileView

#LogoutUserView

urlpatterns = (
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(next_page='index'), name='logout'),
    # path('', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('details/<int:pk>', DetailsProfileView.as_view(), name='profile details'),
    path('update/<int:pk>', UpdateProfileView.as_view(), name='profile update'),
    path('delete/<int:pk>', DeleteProfileView.as_view(), name='profile delete'),
)
