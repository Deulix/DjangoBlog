from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CommentForm, PostForm
from .models import Comment, LikePost, Post, LikeComment
from django.contrib.auth.models import User


def home(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "home.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(parent_comment__isnull=True)
    is_liked_post = post.post_likes.filter(user=request.user).exists() if request.user.is_authenticated else False

    if request.user.is_authenticated:
        for comment in comments:
            comment.is_liked_by_user = comment.comment_likes.filter(user=request.user).exists()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = CommentForm()

    return render(
        request, "post_detail.html", {"post": post, "comments": comments, "form": form, 'is_liked_post':is_liked_post})


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Пост успешно создан!')
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "post_form.html", {"form": form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect("home")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост успешно отредактирован!')
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "post_form.html", {"form": form})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect("home")
    else:
        post.delete()
        messages.success(request, 'Пост успешно удалён!')
        return redirect("home")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.post_likes.filter(user=request.user).exists():
        post.post_likes.filter(user=request.user).delete()
        # messages.info(request, 'Лайк удалён')
    else:
        LikePost.objects.create(post=post, user=request.user)
        # messages.success(request, 'Лайк поставлен')
    return redirect('post_detail', pk=pk)

@login_required
def comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.comment_likes.filter(user=request.user).exists():
        comment.comment_likes.filter(user=request.user).delete()
        # messages.info(request, 'Лайк удалён')
    else:
        LikeComment.objects.create(comment=comment, user=request.user)
        # messages.success(request, 'Лайк поставлен')
    return redirect('post_detail', pk=comment.post.pk)

# @login_required
# def profile(request, pk):
#     profile = get_object_or_404(User, pk=pk)
#     return render(
#         request, "post_detail.html", {"profile":profile}
#     )
