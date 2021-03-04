from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from blogging.models import Post

from django import forms
from django.utils import timezone
from blogging.modelform.forms import MyCommentForm

def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join(["\t%s" % a for a in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join(["\t%s: %s" % i for i in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")

def list_view(request):
    published = Post.objects.exclude(published_date__exact=None)
    posts = published.order_by('-published_date')
    context = {'posts': posts}
    return render(request, 'blogging/list.html', context)

def detail_view(request, post_id):
    published = Post.objects.exclude(published_date__exact=None)

    new_comment = None

    try:
        post = published.get(pk=post_id)
        comments = post.comments
        comment_form = MyCommentForm(data=request.POST)
        if request.method == 'POST':
            if comment_form.is_valid():
                # Create Comment object but don't save to database yet
                new_comment = comment_form.save(commit=False)
                # Assign the current post to the comment
                new_comment.post = post
                # Save the comment to the database
                new_comment.save()
            else:
                comment_form = MyCommentForm()
    except Post.DoesNotExist:
        raise Http404

    context = {'post': post,
                'comments': comments,
                'new_comment': new_comment,
                'comment_form': comment_form}

    return render(request, 'blogging/detail.html', context)
