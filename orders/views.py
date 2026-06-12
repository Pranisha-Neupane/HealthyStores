"""
Checkout flow + the loyalty program logic.
Loyalty rule: when a customer completes their Nth order (N from settings,
default every 5th), a personal 15% promo code is generated automatically.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import transaction
from cart.cart import Cart
from cart.views import _get_session_promo
from .forms import CheckoutForm
from .models import Order, OrderItem, PromoCode


@login_required
def checkout(request):
    """Show the checkout form and create the order on POST."""
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty — add some healthy items first!")
        return redirect('products:menu')

    promo = _get_session_promo(request)
    profile = request.user.profile

    # Pre-fill the form from the user's saved details
    initial = {
        'full_name': request.user.get_full_name() or request.user.username,
        'email': request.user.email,
        'phone': profile.phone,
        'address': profile.address,
    }
    form = CheckoutForm(request.POST or None, initial=initial)

    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            order = form.save(commit=False)
            order.user = request.user
            order.subtotal = cart.subtotal
            order.tax = cart.tax
            order.delivery_charge = cart.delivery
            order.discount = cart.discount(promo)
            order.grand_total = cart.grand_total(promo)
            order.promo_code = promo
            order.save()

            # Freeze each cart line into an OrderItem
            for row in cart:
                OrderItem.objects.create(
                    order=order,
                    product=row['product'],
                    product_name=row['product'].name,
                    price=row['price'],
                    quantity=row['quantity'],
                )

            # Mark the promo as consumed
            if promo:
                promo.used = True
                promo.save()

            # ---------------- LOYALTY PROGRAM ----------------
            profile.total_orders += 1
            profile.save()
            if profile.total_orders % settings.LOYALTY_ORDER_COUNT == 0:
                new_code = PromoCode.generate_for(request.user)
                # Stored in the session so the success page can celebrate
                request.session['loyalty_code'] = new_code.code
                messages.success(
                    request,
                    "Congratulations! You've earned a loyalty discount. "
                    f"Use code {new_code.code} for {new_code.discount_percent}% off your next order! 🎉")

        cart.clear()
        return redirect('orders:success', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart,
        'promo': promo,
        'discount': cart.discount(promo),
        'grand_total': cart.grand_total(promo),
    })


@login_required
def success(request, order_id):
    """Order confirmation page (also shows a new loyalty code if earned)."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    loyalty_code = request.session.pop('loyalty_code', None)
    return render(request, 'orders/success.html', {
        'order': order, 'loyalty_code': loyalty_code})


@login_required
def order_detail(request, order_id):
    """Full invoice view of a single past order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
