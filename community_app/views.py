from django.forms import ModelForm
from django.shortcuts import render, redirect

from community_app import models
from community_app.models import Post, Comment, Subject


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = [
            'name', 'description', 'is_admin'
        ]
        labels = {
            'name': '말머리 명',
            'description': '설명',
            'is_admin': '관리자 전용 여부'
        }


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'subject_id', 'title', 'content'
        ]
        labels = {
            'subject_id': '말머리',
            'title': '제목',
            'content': '내용',
        }

    def __init__(self, user=None, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if user:
            # 관리자의 경우 공지 포함
            if user.is_admin:
                self.fields['subject_id'].queryset = models.Subject.objects.all()
            else:
                self.fields['subject_id'].queryset = models.Subject.objects.filter(is_admin=False)


def index(request):
    context = {}

    if request.user.is_authenticated:
        post_form = PostForm(user=request.user)
        context['post_form'] = post_form

    admin_post_objs = Post.objects.filter(subject_id__is_admin=True)
    context['admin_post_objs'] = admin_post_objs

    post_objs = Post.objects.filter(subject_id__is_admin=False)
    context['post_objs'] = post_objs

    subject_objs = Subject.objects.all
    context['subject_objs'] = subject_objs

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

    subject_objs = Subject.objects.all
    context['subject_objs'] = subject_objs

    if request.user.is_authenticated:
        post_form = PostForm(request.user, request.POST or None, instance=post_obj)
        context['post_form'] = post_form

        if post_form.is_valid():
            post_form.save()
            return redirect(
                post_detail,
                post_id
            )

    return render(
        request,
        'community_app/post_detail.html',
        context,
    )


def add_post(request):
    if request.POST:
        post_form = PostForm(request.user, request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)

            post.created_by = request.user

            post.save()

    return redirect(index)


def del_post(request, post_id):
    if request.POST:
        try:
            post_obj = Post.objects.get(pk=post_id)
            post_obj.delete()

            return redirect(index)
        except:
            print("삭제하려는 게시글의 POST ID 가 존재하지 않습니다")

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


def del_comment(request, post_id):
    if request.POST:
        comment_id = request.POST['comment_id']

        try:
            comment_obj = Comment.objects.get(pk=comment_id)
            comment_obj.delete()
        except:
            print("댓글 삭제 에러: Comment_id 에 해당하는 댓글이 없습니다.")

    return redirect(post_detail, post_id)


def subject_list(request):
    context = {}

    subject_objs = Subject.objects.all

    subject_form = SubjectForm

    context['subject_objs'] = subject_objs
    context['subject_form'] = subject_form

    return render(
        request,
        'community_app/subject_list.html',
        context
    )


def subject_detail(request, subject_id):
    context = {}

    subject_obj = Subject.objects.get(pk=subject_id)

    context['subject_obj'] = subject_obj

    subject_form = SubjectForm(request.POST or None, instance=subject_obj)
    if subject_form.is_valid():
        subject_form.save()
        return redirect(
            subject_detail,
            subject_id
        )

    context['subject_form'] = subject_form

    return render(
        request,
        'community_app/subject_detail.html',
        context,
    )


def add_subject(request):
    if not request.user.is_authenticated:
        print("권한 없는 사용자의 자유게시판 말머리 등록 차단")
        return redirect(index)

    if request.POST:
        subject_form = SubjectForm(request.POST)

        if subject_form.is_valid():
            subject = subject_form.save(commit=False)

            subject.created_by = request.user
            subject.save()

    return redirect(subject_list)


def del_subject(request, subject_id):
    if request.POST:
        try:
            subject_obj = Subject.objects.get(pk=subject_id)
            subject_obj.delete()
        except:
            print("말머리 삭제 에러: subject_id 에 해당하는 댓글이 없습니다.")

    return redirect(subject_list)