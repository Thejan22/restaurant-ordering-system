from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static   # ← Added this

from menu.views import (
    menu_list, 
    add_to_cart, 
    cart_view, 
    remove_from_cart, 
    update_quantity, 
    place_order,
    order_history
)
from accounts.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Menu
    path('', menu_list, name='home'),
    path('menu/', menu_list, name='menu'),
    
    # Cart Features
    path('add-to-cart/<int:food_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('remove-from-cart/<int:food_id>/', remove_from_cart, name='remove_from_cart'),
    path('update-quantity/<int:food_id>/<str:action>/', update_quantity, name='update_quantity'),
    
    # Checkout / Place Order
    path('place-order/', place_order, name='place_order'),
    
    # Order History
    path('order-history/', order_history, name='order_history'),
    
    # User Authentication
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register, name='register'),
]

# ====================== MEDIA FILES (For Food Images) ======================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ===========================================================================