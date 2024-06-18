from django.contrib import admin
from .models import Prod,Category,OrderItem,Order
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}
    list_per_page = 5
admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','stock','available','created','updated']
    list_editable =['price','stock','available']
    prepopulated_fields = {'slug':('name',)}
    list_per_page = 5
admin.site.register(Prod,ProductAdmin)

class OrderItemAdmin(admin.TabularInline):
    model=OrderItem
    fieldsets = [
        ('Product',{'fields':['product'],}),
        ('Quantity',{'fields':['quantity'],}),
        ('Price',{'fields':['price'],}),
    ]
    readonly_fields = ['product','quantity','price']
@admin.register(Order)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','emailAddress','created']
    list_display_links = ['id']
    search_fields = ['id','emailAddress']
    readonly_fields = ['id','token','total','emailAddress','created','total','token_type']
    fieldsets = [
        ('ORDER_INFORMATION',{'fields':['id','token','total','created']})
    ]
    inlines = [
        OrderItemAdmin,
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
