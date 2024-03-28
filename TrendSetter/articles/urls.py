from django.urls import path

# urlpatterns = (
#     path("create/", PetCreateView.as_view(), name="create pet"),
#     path("<str:username>/pet/<slug:pet_slug>/",
#          include([
#              path("", PetDetailView.as_view(), name='details pet'),
#              path("edit/", PetEditView.as_view(), name='edit pet'),
#              path("delete/", PetDeleteView.as_view(), name='delete pet'),
#          ])),
# )

from django.urls import path
from .views import (
    EducationArticleCreateView,
    EducationArticleUpdateView,
    EducationArticleDetailView,
    AllArticlesView,
)

urlpatterns = [
    # Other URL patterns
    path('create-article/', EducationArticleCreateView.as_view(), name='create article'),
    path('update-article/<slug:article_slug>/', EducationArticleUpdateView.as_view(), name='update article'),
    path('article/<slug:article_slug>/', EducationArticleDetailView.as_view(), name='article details'),
  #  path('articles/<int:pk>/', EducationArticleListView.as_view(), name='article list'),
    path('education/', AllArticlesView.as_view(), name='education articles'),
]
