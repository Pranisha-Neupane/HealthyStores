"""Feedback app — star ratings + reviews from customers."""
from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):
    RATING_CHOICES = [(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(
        default=True, help_text="Uncheck to hide a review from the website")

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Feedback'

    def __str__(self):
        return f"{self.user.username} — {self.rating}★"

    @property
    def stars(self):
        """Range helper so templates can loop filled stars."""
        return range(self.rating)

    @property
    def empty_stars(self):
        return range(5 - self.rating)
