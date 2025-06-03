from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CommentForm, PostForm
from .models import Comment, LikePost, Post, LikeComment
from django.contrib.auth.models import User


def home(request):
    posts = Post.objects.all().order_by("-created_at")

    liked_posts_ids = []
    if request.user.is_authenticated:
        liked_posts_ids = list(
            LikePost.objects.filter(user=request.user, post__in=posts).values_list(
                "post_id", flat=True
            )
        )

    return render(
        request, "home.html", {"posts": posts, "liked_posts_ids": liked_posts_ids}
    )


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(parent_comment__isnull=True)
    is_liked_post = (
        post.likes.filter(user=request.user).exists()
        if request.user.is_authenticated
        else False
    )

    if request.user.is_authenticated:
        for comment in comments:
            comment.is_liked_by_user = comment.likes.filter(user=request.user).exists()

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
        request,
        "post_detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "is_liked_post": is_liked_post,
        },
    )


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Пост успешно создан!")
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
            messages.success(request, "Пост успешно отредактирован!")
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "post_form.html", {"form": form})

@login_required
def post_delete(request, pk):
    # if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return redirect("home")
        else:
            post.delete()
            messages.success(request, "Пост успешно удалён!")
            return redirect("home")
    # else:
    #     return redirect("home")

@login_required
def comment_delete(request, pk):
    if request.method == "POST":
        comment = get_object_or_404(Comment, pk=pk)
        if comment.author != request.user:
            return redirect("home")
        else:
            comment.delete()
            messages.success(request, "Комментарий успешно удалён!")
            return redirect("post_detail", pk=comment.post.pk)
    else:
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
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        if post.likes.filter(user=request.user).exists():
            post.likes.filter(user=request.user).delete()
        else:
            LikePost.objects.create(post=post, user=request.user)
        return redirect("post_detail", pk=pk)
    else:
        return redirect("home")


@login_required
def post_like_home(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        if post.likes.filter(user=request.user).exists():
            post.likes.filter(user=request.user).delete()
        else:
            LikePost.objects.create(post=post, user=request.user)
        return redirect("home")
    else:
        return redirect("home")


@login_required
def comment_like(request, pk):
    if request.method == "POST":
        comment = get_object_or_404(Comment, pk=pk)
        if comment.likes.filter(user=request.user).exists():
            comment.likes.filter(user=request.user).delete()
        else:
            LikeComment.objects.create(comment=comment, user=request.user)
        return redirect("post_detail", pk=comment.post.pk)
    else:
        return redirect("home")


# @login_required
# def profile(request, pk):
#     profile = get_object_or_404(User, pk=pk)
#     return render(
#         request, "post_detail.html", {"profile":profile}
#     )
