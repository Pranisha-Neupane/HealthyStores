"""Cart pages and actions: add / remove / update / apply promo."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from products.models import Product
from orders.models import PromoCode
from .cart import Cart


def cart_detail(request):
    """Cart page with totals and promo-code form."""
    cart = Cart(request)
    promo = _get_session_promo(request)
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'promo': promo,
        'discount': cart.discount(promo),
        'grand_total': cart.grand_total(promo),
    })


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product, quantity)
    messages.success(request, f"Added {product.name} to your cart 🛒")
    # Return to wherever the user was
    return redirect(request.POST.get('next') or 'cart:detail')


@require_POST
def cart_update(request, product_id):
    """Set an exact quantity from the cart page (+ / − buttons)."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product, quantity, override=True)
    return redirect('cart:detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f"Removed {product.name} from your cart.")
    return redirect('cart:detail')


@require_POST
def apply_promo(request):
    """Validate a promo code and remember it in the session."""
    code = request.POST.get('code', '').strip().upper()
    try:
        promo = PromoCode.objects.get(code=code, used=False)
        if request.user.is_authenticated and promo.user and promo.user != request.user:
            raise PromoCode.DoesNotExist
        request.session['promo_code'] = promo.code
        messages.success(request, f"Promo code applied — {promo.discount_percent}% off! 🎉")
    except PromoCode.DoesNotExist:
        request.session.pop('promo_code', None)
        messages.error(request, "Invalid or already-used promo code.")
    return redirect('cart:detail')


def remove_promo(request):
    request.session.pop('promo_code', None)
    messages.info(request, "Promo code removed.")
    return redirect('cart:detail')


def _get_session_promo(request):
    """Helper: return the PromoCode object stored in the session (or None)."""
    code = request.session.get('promo_code')
    if not code:
        return None
    return PromoCode.objects.filter(code=code, used=False).first()
