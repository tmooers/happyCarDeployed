from django.conf import settings
from shop.models import Part
from decimal import Decimal

class Cart(object):

    def __init__(self,request):
        self.session=request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart=self.session[settings.CART_SESSION_ID] = {}

        self.cart=cart

    def add(self,part,quantity=1,override_quantity=False):
        part_id = str(part.id)

        if part_id not in self.cart:
            self.cart[part_id]={'quantity':0, 'price':str(part.price)}

        if override_quantity:
            self.cart[part_id]['quantity']=quantity
        else:
            self.cart[part_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self,part):
        part_id = str(part.id)
        if part_id in self.cart:
            del self.cart[part_id]
            self.save()


    def __iter__(self):
        part_ids = self.cart.keys()
        parts = Part.objects.filter(id__in=part_ids)

        cart = self.cart.copy()
        for part in parts:
            cart[str(part.id)]['part'] = part

        for item in cart.values():
            item['price']=Decimal(item['price'])
            item['total_price']=item['price'] * item['quantity']
            yield item


    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())


    def get_total_price(self):
        return sum(Decimal(item['price'])* item['quantity'] for item in self.cart.values())


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()