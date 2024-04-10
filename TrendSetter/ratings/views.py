from django.contrib import messages
from django.shortcuts import render, redirect

from TrendSetter.ratings.forms import CommentForm
from TrendSetter.ratings.models import CommentRating


# Create your views here.
#
# def submit_comment(request,pk):
#     url = request.META,get('HTTP_REFERER')
#     if request.method == 'POST':
#         try:
#             comments = CommentRating.objects.get(user__pk=request.user.pk, article_pk=pk)
#             form = CommentForm(request.POST, instance = comments)
#             form.save()
#             messages.success(request, 'Thank you! Your review has been updated!')
#             return redirect(url)
#
#         except: CommentRating.DoesNotExist:
#             form = CommentForm(request.POST)
#             if form.is_valid():
#                 data = CommentRating()
#                 data.rating = form.cleaned_data['rating']
#                 data.comment = form.cleaned_data['comment']
#                 data.ip_address = request.META.get['REMOTE_ADDR']
#                 data.article_pk = article.pk
#
#                 data.save()


