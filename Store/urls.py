
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home,name="Home"),
    path('category/<slug:category_slug>',views.home,name='product_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>', views.aboutpage,name="product_details"),
    path('cart/add/<int:product_id>',views.add_cart,name='add_cart'),
    path('cart',views.cart_detail,name='cart_detail'),
    path('cart/remove/<int:product_id>',views.cart_remove,name='cart_remove'),
    path('cart/remove_product/<int:product_id>',views.cart_remove_product,name='cart_remove_product'),
    path('thankyou/<int:order_id>',views.thanks_page,name='thank_you'),
    path('search/',views.search,name='search'),
]
