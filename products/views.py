"""Public pages: homepage, full menu, product detail, contact."""
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Category, Product
from .forms import ContactForm


def home(request):
    """Homepage — hero + featured items + every category preview."""
    categories = Category.objects.prefetch_related('products')
    featured = Product.objects.filter(featured=True, available=True)[:6]
    return render(request, 'products/home.html', {
        'categories': categories,
        'featured': featured,
    })


def menu(request):
    """Full menu grouped by category with horizontal scroll rows."""
    categories = Category.objects.prefetch_related('products')
    return render(request, 'products/menu.html', {'categories': categories})


def detail(request, slug):
    """Single product page."""
    product = get_object_or_404(Product, slug=slug, available=True)
    related = product.category.products.exclude(pk=product.pk)[:4]
    return render(request, 'products/detail.html', {
        'product': product, 'related': related})


def contact(request):
    """Contact page with a simple form (prints to console / saves nothing)."""
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        # In production you would email this; here we just confirm.
        messages.success(request, "Thank you! We received your message and will reply soon.")
        form = ContactForm()  # reset the form
    return render(request, 'products/contact.html', {'form': form})
