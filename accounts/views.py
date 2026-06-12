"""Registration, profile and order-history views.
Login / logout / password-reset use Django's built-in class views (see urls.py)."""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileForm
from orders.models import Order, PromoCode


def register(request):
    """Create a new account and log the user in immediately."""
    if request.user.is_authenticated:
        return redirect('products:home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Welcome to Healthy Bites, {user.username}! 🎉")
        return redirect('products:home')
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    """View / edit personal details + see available promo codes."""
    form = ProfileForm(request.POST or None, instance=request.user.profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('accounts:profile')
    promo_codes = PromoCode.objects.filter(user=request.user, used=False)
    # Loyalty progress towards the next reward (every 5th order)
    from django.conf import settings
    n = settings.LOYALTY_ORDER_COUNT
    progress = request.user.profile.total_orders % n
    return render(request, 'accounts/profile.html', {
        'form': form,
        'promo_codes': promo_codes,
        'loyalty_progress': progress,
        'loyalty_percent': int(progress / n * 100),
        'orders_to_reward': n - progress,
    })


@login_required
def order_history(request):
    """List every order the user has placed, newest first."""
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'accounts/order_history.html', {'orders': orders})
