from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'comment', 'approved', 'created_at')
    list_filter = ('rating', 'approved')
    list_editable = ('approved',)
    search_fields = ('user__username', 'comment')
