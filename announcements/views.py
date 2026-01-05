from django.shortcuts import render, get_object_or_404, redirect
from .models import Announcement
from .forms import CommentForm


def home(request):
    return render(request, 'home.html')


def announcement_list(request):
    qs = Announcement.objects.order_by('-created_at')
    return render(request, 'announcements/list.html', {'announcements': qs})


def announcement_detail(request, id):
    announcement = get_object_or_404(Announcement, pk=id)
    comments = announcement.comments.all().order_by('-created_at')

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.announcement = announcement
            comment.save()
            return redirect("announcement_detail", id=announcement.id)
    else:
        form = CommentForm()

    return render(
        request,
        "announcements/detail.html",
        {
            "announcement": announcement,
            "comments": comments,
            "form": form,
        }
    )
