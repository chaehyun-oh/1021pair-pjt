from django.shortcuts import render, redirect
from .models import Review, Comment
from .forms import CommentForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.


def index(request):
    reviews = Review.objects.order_by("-pk")
    context = {"reviews": reviews}
    return render(request, "reviews/index.html", context)


def detail(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm()
    context = {
        "review": review,
        "comments": review.comment_set.all(),
        "comment_form": comment_form,
    }
    return render(request, "reviews/detail.html", context)


def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "글 작성이 완료되었습니다.")
            return redirect("reviews:index")
    else:
        review_form = ReviewForm()
    context = {"review_form": review_form}
    return render(request, "reviews/form.html", context)


def update(request, pk):
    pass


def delete(request, pk):
    pass


@login_required
def comment_create(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
    return redirect("reviews:detail", pk)


def comment_delete(request, pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
        messages.warning(request, "댓글이 삭제되었습니다.")
    return redirect("reviews:detail", pk)
