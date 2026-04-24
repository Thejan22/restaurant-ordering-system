from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import FoodItem, Order   # Order is imported

def menu_list(request):
    food_items = FoodItem.objects.filter(is_available=True)
    return render(request, 'menu/menu_list.html', {
        'food_items': food_items,
    })

def add_to_cart(request, food_id):
    food = get_object_or_404(FoodItem, id=food_id)
    
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    cart = request.session['cart']
    food_id_str = str(food_id)
    
    if food_id_str in cart:
        cart[food_id_str]['quantity'] += 1
    else:
        cart[food_id_str] = {
            'name': food.name,
            'price': float(food.price),
            'quantity': 1
        }
    
    request.session.modified = True
    messages.success(request, f"✅ {food.name} added to your cart!")
    return redirect('menu')

@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    total = 0
    cart_items = []
    
    for food_id, item in cart.items():
        item_total = item['price'] * item['quantity']
        total += item_total
        cart_items.append({
            'food_id': food_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'item_total': item_total
        })
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart/cart.html', context)

@login_required
def remove_from_cart(request, food_id):
    if 'cart' in request.session:
        cart = request.session['cart']
        food_id_str = str(food_id)
        if food_id_str in cart:
            item_name = cart[food_id_str]['name']
            del cart[food_id_str]
            request.session.modified = True
            messages.success(request, f"{item_name} removed from cart.")
    
    return redirect('cart')

@login_required
def update_quantity(request, food_id, action):
    if 'cart' in request.session:
        cart = request.session['cart']
        food_id_str = str(food_id)
        
        if food_id_str in cart:
            if action == 'increase':
                cart[food_id_str]['quantity'] += 1
            elif action == 'decrease':
                cart[food_id_str]['quantity'] -= 1
                if cart[food_id_str]['quantity'] < 1:
                    del cart[food_id_str]
                    messages.success(request, "Item removed from cart.")
                    request.session.modified = True
                    return redirect('cart')
            
            request.session.modified = True
            messages.success(request, "Cart updated!")
    
    return redirect('cart')

# ==================== PLACE ORDER (Now Saves to Database) ====================
@login_required
def place_order(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect('cart')
    
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    
    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address', '').strip()
        
        if not delivery_address:
            messages.error(request, "Please enter a delivery address.")
            return redirect('place_order')
        
        # Save the Order to Database
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            delivery_address=delivery_address,
            status='Pending'
        )
        
        # Clear the cart after successful order
        request.session['cart'] = {}
        request.session.modified = True
        
        messages.success(request, f"🎉 Order #{order.id} placed successfully! Total: Rs. {total:.2f}")
        return redirect('menu')
    
    # Show checkout form
    context = {
        'cart': cart,
        'total': total,
    }
    return render(request, 'cart/place_order.html', context)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'accounts/order_history.html', {'orders': orders})