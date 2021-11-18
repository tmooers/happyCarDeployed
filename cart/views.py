from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from shop.models import Part
from .forms import CartAddProductForm

@require_POST
def cart_add(request,part_id):
    cart = Cart(request)
    part = get_object_or_404(Part, id=part_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(part=part, quantity=cd['quantity'], override_quantity=cd['override'])

    return redirect ('cart:cart_detail')


def cart_remove(request,part_id):
    cart = Cart(request)
    part = get_object_or_404(Part, id=part_id)
    cart.remove(part)

    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request,'cart/detail.html',{'cart':cart})