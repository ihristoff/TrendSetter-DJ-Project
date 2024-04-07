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
    EducationalArticleCreateView,
    EducationalArticleUpdateView,
    EducationalArticleDetailView,
    AllArticlesView,
)

urlpatterns = [
    # Other URL patterns
    path('create-article/', EducationalArticleCreateView.as_view(), name='create article'),
    path('update-article/<slug:article_slug>/', EducationalArticleUpdateView.as_view(), name='update article'),
    path('article/<slug:article_slug>/', EducationalArticleDetailView.as_view(), name='article details'),
  #  path('articles/<int:pk>/', EducationArticleListView.as_view(), name='article list'),
    path('education/', AllArticlesView.as_view(), name='education articles'),
]
