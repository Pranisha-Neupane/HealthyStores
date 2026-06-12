"""
Products app models
===================
Category  -> groups items (Healthy Food, Drinks, Snacks, Protein Bars)
Product   -> a single menu item with nutrition info
"""
from django.db import models
from django.urls import reverse


class Category(models.Model):
    """A menu section, e.g. 'Healthy Drinks'."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    icon = models.CharField(
        max_length=50, blank=True,
        help_text="Bootstrap icon class, e.g. 'bi-cup-straw'")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['display_order']

    def __str__(self):
        return self.name


class Product(models.Model):
    """A single food / drink item shown on the menu."""
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(blank=True)
    ingredients = models.TextField(
        blank=True, help_text="Comma-separated list, e.g. 'Avocado, Lemon'")
    protein = models.CharField(max_length=20, blank=True, help_text="e.g. 12g")
    fiber = models.CharField(max_length=20, blank=True, help_text="e.g. 9g")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    emoji = models.CharField(
        max_length=10, blank=True, default='🥗',
        help_text="Shown as a placeholder when no image is uploaded")
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category__display_order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.slug])

    @property
    def ingredient_list(self):
        """Return ingredients as a clean Python list for templates."""
        return [i.strip() for i in self.ingredients.split(',') if i.strip()]
