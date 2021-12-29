from django.forms import ModelForm
from django.shortcuts import render, redirect

from community_app.models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'category_id', 'title', 'content'
        ]
        labels = {
            'category_id': '말머리',
            'title': '제목',
            'content': '내용',
        }


def index(request):
    context = {}

    post_form = PostForm

    post_objs = Post.objects.all

    context['post_form'] = post_form

    context['post_objs'] = post_objs

    return render(
        request,
        'community_app/index.html',
        context,
    )


def post_detail(request, post_id):
    context = {}

    post_obj = Post.objects.get(pk=post_id)
    comment_objs = Comment.objects.filter(post_id=post_obj)

    context['post_obj'] = post_obj
    context['comment_objs'] = comment_objs

    return render(
        request,
        'community_app/post_detail.html',
        context,
    )


def add_post(request):
    if request.POST:
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)

            post.created_by = request.user

            post.save()

    return redirect(index)


def add_comment(request, post_id):
    if request.POST:
        comment = request.POST['comment']
        post_obj = Post.objects.get(pk=post_id)

        comment_obj = Comment.objects.create(
            post_id=post_obj,
            comment=comment,
            created_by=request.user
        )

    return redirect(post_detail, post_id)
