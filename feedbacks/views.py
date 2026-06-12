"""Feedback page: submit (login required) + display approved reviews."""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg
from .models import Feedback
from .forms import FeedbackForm


def feedback(request):
    form = FeedbackForm(request.POST or None)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to leave a review.")
            return redirect('accounts:login')
        if form.is_valid():
            fb = form.save(commit=False)
            fb.user = request.user
            fb.save()
            messages.success(request, "Thank you for your feedback! 💚")
            return redirect('feedbacks:feedback')

    reviews = Feedback.objects.filter(approved=True).select_related('user')
    avg = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    return render(request, 'feedbacks/feedback.html', {
        'form': form,
        'reviews': reviews,
        'avg_rating': round(avg, 1),
        'review_count': reviews.count(),
    })
