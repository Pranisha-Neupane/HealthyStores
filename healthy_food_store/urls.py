"""Root URL configuration — routes requests to each app."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('feedback/', include('feedbacks.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin site branding
admin.site.site_header = "Healthy Bites & Refreshers — Admin"
admin.site.site_title = "Healthy Bites Admin"
admin.site.index_title = "Store Management Dashboard"
