"""Makes the cart item count available in every template (navbar badge)."""
from .cart import Cart


def cart_counter(request):
    return {'cart_count': len(Cart(request))}
