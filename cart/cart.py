"""
Session-based shopping cart
===========================
The cart lives in request.session['cart'] as:
    { "<product_id>": {"quantity": 2}, ... }
Prices are always read fresh from the database so they can never go stale.
"""
from decimal import Decimal
from django.conf import settings
from products.models import Product

CART_SESSION_KEY = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    # ---------- mutations ----------
    def add(self, product, quantity=1, override=False):
        """Add a product or update its quantity."""
        pid = str(product.id)
        if pid not in self.cart:
            self.cart[pid] = {'quantity': 0}
        if override:
            self.cart[pid]['quantity'] = quantity
        else:
            self.cart[pid]['quantity'] += quantity
        # Never allow zero/negative quantities
        if self.cart[pid]['quantity'] <= 0:
            del self.cart[pid]
        self.save()

    def remove(self, product):
        pid = str(product.id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.session.pop('promo_code', None)
        self.session.modified = True

    def save(self):
        self.session.modified = True

    # ---------- iteration / totals ----------
    def __iter__(self):
        """Yield cart rows with live product objects and line totals."""
        products = Product.objects.filter(id__in=self.cart.keys())
        for product in products:
            item = self.cart[str(product.id)]
            quantity = item['quantity']
            yield {
                'product': product,
                'quantity': quantity,
                'price': product.price,
                'total': product.price * quantity,
            }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def subtotal(self):
        return sum(row['total'] for row in self)

    @property
    def tax(self):
        return (self.subtotal * Decimal(str(settings.TAX_RATE))).quantize(Decimal('0.01'))

    @property
    def delivery(self):
        if not self.cart:
            return Decimal('0')
        if self.subtotal >= settings.FREE_DELIVERY_ABOVE:
            return Decimal('0')
        return Decimal(str(settings.DELIVERY_CHARGE))

    def discount(self, promo=None):
        """Rupee value of a promo discount applied to the subtotal."""
        if promo:
            return (self.subtotal * Decimal(promo.discount_percent) / 100).quantize(Decimal('0.01'))
        return Decimal('0')

    def grand_total(self, promo=None):
        return self.subtotal + self.tax + self.delivery - self.discount(promo)
