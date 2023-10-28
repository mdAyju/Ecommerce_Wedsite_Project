from django.contrib import admin
from app.models import Product,Customer,Cart,Payment,OrderPlaced,Whishlist

# admin.site.register(Product)

@admin.register(Product)
class ProductModel(admin.ModelAdmin):
    list_display= ['id','title','discount_price','category','product_image']

@admin.register(Customer)
class CustomerModel(admin.ModelAdmin):
    list_display= ['id','user','name','locality','city','state','zipcode',]


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display=['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','Customer','product','quantity','ordered_date','status','payment']

@admin.register(Whishlist)
class WhishliatModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product']