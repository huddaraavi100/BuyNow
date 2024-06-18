from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Prod,Cart,Cartitem,Order,OrderItem
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
# Create your views here.
def home(request,category_slug=None):
    category_page=None
    products=None
    if category_slug!=None:
        category_page=get_object_or_404(Category, slug=category_slug)
        products=Prod.objects.filter(category=category_page,available=True)
    else:
        products=Prod.objects.all().filter(available=True)
    return render(request,'home.html',{'category':category_page,'products':products})

def aboutpage(request,category_slug,product_slug):
    try:
        product=Prod.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'about.html',{'product':product})

def cart(request):
    return render(request,'cart.html')

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
    product=Prod.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()
    try:
        cart_item=Cartitem.objects.get(product=product,cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity +=1
        cart_item.save()
    except Cartitem.DoesNotExist:
        cart_item=Cartitem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    return redirect('cart_detail')

def cart_detail(request,total=0,counter=0,cart_items=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=Cartitem.objects.filter(cart=cart,active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            counter+=cart_item.quantity
    except ObjectDoesNotExist:
        pass
    stripe.api_key=settings.STRIPE_SECRET_KEY
    stripe_total=int(total+100)
    description='BuyNow - New Order'
    data_key=settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        #print(request.POST)
        try:
            token=request.POST['stripeToken']
            email=request.POST['stripeEmail']
            token_type=request.POST['stripeTokenType']

            customer=stripe.Customer.create(
                email=email,
                source=token
            )
            charge=stripe.Charge.create(
                amount=stripe_total,
                currency='inr',
                description=description,
                customer=customer.id
            )
            try:
                order_details=Order.objects.create(
                    token=token,
                    total=total,
                    emailAddress=email,
                    token_type=token_type
                )
                order_details.save()
                for order_item in cart_items:
                    or_item=OrderItem.objects.create(
                        product=order_item.product.name,
                        quantity=order_item.quantity,
                        price=order_item.product.price,
                        order=order_details
                    )
                    or_item.save()
                    products=Prod.objects.get(id=order_item.product.id)
                    products.stock=int(order_item.product.stock-order_item.quantity)
                    products.save()
                    order_item.delete()

                    print('Order has been created')
                return redirect('thank_you',order_details.id)
            except ObjectDoesNotExist:
                pass
        except stripe.error.CardError as e:
            return False,e
    return render(request,'cart.html',dict(cart_items=cart_items,total=total,counter=counter,data_key=data_key,stripe_total=stripe_total,description=description))

def cart_remove(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Prod,id=product_id)
    cart_item=Cartitem.objects.get(product=product,cart=cart)
    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

def cart_remove_product(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Prod,id=product_id)
    cart_item=Cartitem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart_detail')

def thanks_page(request,order_id):
    if order_id:
        customer_order=get_object_or_404(Order,id=order_id)
    return render(request,'thankyou.html',{'customer_order':customer_order})

def search(request):
    #print(request.GET['name'])
    products=Prod.objects.filter(name__contains=request.GET.get('title'))
    #print(products)
    return render(request,'home.html',{'products':products})
