from .models import Cart,Cartitem
# from account.models import Logo
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart    


def counter(request):
    cart_count=0
    if 'admin' in request.path:
        return {}

    else:
        try:
            cart=Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items=Cartitem.objects.all().filter(user=request.user)


            else:    
               cart_items=Cartitem.objects.all().filter(cart=cart[:1])
            for item in cart_items:
                cart_count=cart_count+item.quantity

        except Cart.DoesNotExist:
            cart_count=0
    return dict(cart_count=cart_count)  