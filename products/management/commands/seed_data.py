"""
Seed the database with the full Healthy Bites menu.
Run:  python manage.py seed_data
Safe to re-run — existing items are updated, not duplicated.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category, Product

MENU = {
    ('Featured Healthy Food', 'bi-egg-fried', 1): [
        dict(name='Avocado Toast with Cabbage and Radish Slices', price=450,
             ingredients='Avocado, Whole grain bread, Cabbage, Radish, Lemon, Olive oil',
             protein='12g', fiber='9g', emoji='🥑', featured=True,
             description='Creamy avocado on toasted whole grain bread, topped with crunchy cabbage and radish.'),
        dict(name='Egg and Cucumber Spaghetti Katti Roll', price=350,
             ingredients='Egg, Cucumber, Whole wheat wrap, Lettuce, Tomato',
             protein='18g', fiber='7g', emoji='🌯', featured=True,
             description='Protein-rich egg and fresh cucumber rolled in a soft whole wheat wrap.'),
        dict(name='Healthy Veggie Bowl', price=450,
             ingredients='Tomatoes, Onions, Beetroot, Lettuce, Carrots',
             protein='15g', fiber='10g', emoji='🥗', featured=True,
             description='A rainbow bowl of garden-fresh vegetables, lightly dressed.'),
    ],
    ('Healthy Drinks', 'bi-cup-straw', 2): [
        dict(name='Iced Cucumber with Rock Salt, Lemon & Mint', price=150, emoji='🥒',
             ingredients='Cucumber, Rock salt, Lemon, Mint',
             description='Ultra-refreshing iced cooler with a zesty mineral kick.'),
        dict(name='Iced Beetroot Juice with Rock Salt & Lemon', price=200, emoji='🟥',
             ingredients='Beetroot, Rock salt, Lemon',
             description='Earthy, vibrant and packed with natural nitrates.'),
        dict(name='Mango Milkshake', price=250, emoji='🥭',
             ingredients='Mango, Milk',
             description='Thick, creamy shake made with ripe seasonal mangoes.'),
        dict(name='Strawberry Refresher', price=200, emoji='🍓',
             ingredients='Strawberry, Lemon, Mint',
             description='Sweet-tart strawberry refresher served chilled.'),
        dict(name='Lemon Ginger Refreshing Drink', price=160, emoji='🍋',
             ingredients='Lemon, Ginger, Honey',
             description='Immunity-boosting zing of fresh ginger and lemon.'),
        dict(name='Oats Drink Cooked in Milk', price=450, emoji='🥛', featured=True,
             ingredients='Oats, Milk, Chia Seeds, Pumpkin Seeds, Sunflower Seeds, Dried Grapes',
             protein='14g', fiber='8g',
             description='Hearty oats slow-cooked in milk with a superfood seed mix.'),
    ],
    ('Quick Snacks', 'bi-lightning-charge', 3): [
        dict(name='Air Fried Banana Chips', price=300, emoji='🍌',
             ingredients='Banana, Rock salt', fiber='4g',
             description='Crispy, guilt-free banana chips — air fried, never deep fried.'),
        dict(name='Air Fried French Fries', price=200, emoji='🍟',
             ingredients='Potato, Olive oil, Herbs', fiber='3g',
             description='Golden fries with 80% less oil, seasoned with herbs.'),
        dict(name='Air Fried Sweet Potato Chips', price=300, emoji='🍠',
             ingredients='Sweet potato, Olive oil, Paprika', fiber='5g',
             description='Naturally sweet, crunchy chips rich in beta-carotene.'),
    ],
    ('Protein Bars & Laddoo', 'bi-heart-pulse', 4): [
        dict(name='Sunflower & Pumpkin Seeds Laddoo Dipped in Honey', price=550, emoji='🍯',
             ingredients='Sunflower seeds, Pumpkin seeds, Honey',
             protein='16g', fiber='6g', featured=True,
             description='Traditional laddoo reinvented with power seeds and raw honey.'),
        dict(name='Pistachio, Fig & Dates Protein Bar', price=500, emoji='🍫',
             ingredients='Pistachio, Fig, Dates',
             protein='20g', fiber='7g', featured=True,
             description='No-added-sugar bar — natural sweetness from figs and dates.'),
    ],
}


class Command(BaseCommand):
    help = 'Seed categories and products for Healthy Bites & Refreshers'

    def handle(self, *args, **options):
        for (cat_name, icon, order), items in MENU.items():
            category, _ = Category.objects.update_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name), 'icon': icon, 'display_order': order})
            for item in items:
                Product.objects.update_or_create(
                    slug=slugify(item['name']),
                    defaults={'category': category, **item})
            self.stdout.write(self.style.SUCCESS(f"✓ {cat_name}: {len(items)} items"))
        self.stdout.write(self.style.SUCCESS('Menu seeded successfully!'))
