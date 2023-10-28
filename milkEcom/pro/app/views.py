from django.shortcuts import render,redirect,HttpResponseRedirect
import razorpay
from django.views import View
from app.models import Product,Customer,Cart,Payment,OrderPlaced,Whishlist
from app.forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.

def main(request):
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlist=len(Whishlist.objects.filter(user=request.user))
    return render(request,'main.html',locals())

class CategoryView(View):
    def get(self,request,val):
        wishlist=0
        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        if request.user.is_authenticated:
            wishlist=len(Whishlist.objects.filter(user=request.user))
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'category.html',locals())

class categorytitle(View):
    def get(self,request,val):
        wishlist=0
        product=Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishlist=len(Whishlist.objects.filter(user=request.user))
        return render(request,'category.html',locals())


class productDetails(View):
    def get(self,request,pk):
        # import pdb;pdb.set_trace()
        wishlist=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishlist=len(Whishlist.objects.filter(user=request.user))
        product=Product.objects.get(pk=pk)
        wishlists=Whishlist.objects.filter(Q(user=request.user) & Q(product=product))
        return render(request,'productdetails.html',locals())

def about(request):
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        wishlist=len(Whishlist.objects.filter(user=request.user))
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,'about.html',locals())

def contact(request):
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlist=len(Whishlist.objects.filter(user=request.user))

    return render(request,'contact.html',locals())

class customerRegistrationview(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'customerRegistration.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratulaions user register Successfully')
        else:
            messages.warning(request,'Invalid Input Data')
        return render(request,'customerRegistration.html',locals())
    
class ProfileView(View):
    def get(self,request):
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            wishlist=len(Whishlist.objects.filter(user=request.user))
            totalitem=len(Cart.objects.filter(user=request.user))
        form=CustomerProfileForm()
        return render(request,'profile.html',locals())
    
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            res=Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            res.save()
            messages.success(request,'Congratulaions Profile Saved Successfully')
        else:
            messages.warning(request,'Invalid input')
        return render(request,'profile.html',locals())

@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        wishlist=len(Whishlist.objects.filter(user=request.user))
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,'address.html',locals())

class addressUpdate(View):
    def get(self,request,pk):
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            wishlist=len(Whishlist.objects.filter(user=request.user))
            totalitem=len(Cart.objects.filter(user=request.user))
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request,'AddressUpdate.html',locals())
    
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.city=form.cleaned_data['city']
            add.locality=form.cleaned_data['locality']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,'Congratulation! Your Profile Updated Successfully')
        else:
            messages.warning(request,'Invalid Input Data')
        # return render(request,'AddressUpdate.html',locals())
        return redirect('address')
        
def addtocart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

def showcart(request):
    wishlist=0
    user=request.user
    cart=Cart.objects.filter(user=user)
    if request.user.is_authenticated:
        wishlist=len(Whishlist.objects.filter(user=request.user))
        totalitem=len(Cart.objects.filter(user=request.user))
    amount=0
    for p in cart:
        value=p.quantity *p.product.discount_price
        amount=round(amount+value,2)
    totalamount=round(40+amount,2)
    return render(request,'addtocart.html',locals())

def plus_cart(request):
    # import pdb;pdb.set_trace()
    if request.method =='GET':
        prod_id=request.GET.get('prod_id')
        print(prod_id)
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discount_price
            amount=round(amount+value,2)
        totalamount=amount+40
        print(c)
        jsonResponse={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount,
        }
        return JsonResponse(jsonResponse)
    
def minus_cart(request):
    if request.method =='GET':
        prod_id=request.GET.get('prod_id')
        print(prod_id)
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discount_price
            amount=round(amount+value,2)
        totalamount=amount+40
        print(c)
        jsonResponse={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount,
        }
        return JsonResponse(jsonResponse)

def remove_cart(request):
    # import pdb;pdb.set_trace()
    if request.method=='GET':
        prod_id=request.GET.get('prod_id')
        c=Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.delete()
        cart = Cart.objects.filter(user=request.user)
        amount=0
        for p in cart:
            value=p.quantity * p.product.discount_price
            amount= round(amount+value,2)
        totalamount=amount+40
        jsonResponse={
            'amount':amount,
            'totalamount':totalamount
        }
    return JsonResponse(jsonResponse)

class Checkout(View):
    def get(self,request):
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishlist=len(Whishlist.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value=p.quantity *p.product.discount_price
            famount+=value
        totalamount=40+famount
        razoramount=int(totalamount*100)
        client=razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data={'amount':razoramount,'currency':'INR','receipt':'order_rcptid_11'}
        payment_response=client.order.create(data=data)
        print(payment_response)
        # {'id': 'order_MfXMcBmZrwnlPZ', 'entity': 'order', 'amount': 37500, 'amount_paid': 0, 
        # 'amount_due': 37500, 'currency': 'INR', 'receipt': 'order_rcptid_11',
        #  'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1695419746}
        order_id=payment_response['id']
        order_status=payment_response['status']
        if order_status =='created':
            payment= Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        return render(request,'checkout.html',locals())

def payment_done(request):
    # import pdb;pdb.set_trace()
    order_id= request.GET.get('order_id')
    payment_id= request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    user=request.user
    customer =Customer.objects.filter(id=cust_id).first()
    print(customer)

    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid=True
    payment.razorpay_payment_id=payment_id
    payment.save()

    cart= Cart.objects.filter(user=customer.user)
    for c in cart:
        OrderPlaced(user=customer.user,Customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect('order')
        
def order(request):
    totalitem=0
    if request.user.is_authenticated:
        wishlist=len(Whishlist.objects.filter(user=request.user))
        totalitem=len(Cart.objects.filter(user=request.user))
    order_placed= OrderPlaced.objects.filter(user=request.user)
    return render(request,'order.html',locals())


def pluswishlist(request):
    if request.method=='GET':
        prod_id= request.GET['prod_id']
        user=request.user
        product =Product.objects.get(id=prod_id)
        Whishlist(user=user,product=product).save()
        jsonData={
            'message':'Whishlist added successfully'
        }
        return JsonResponse(jsonData)


def minuswhishlist(request):
    # import pdb;pdb.set_trace()
    if request.method=='GET':
        prod_id= request.GET['prod_id']
        user=request.user
        product =Product.objects.get(id=prod_id)
        Whishlist.objects.filter(user=user,product=product).delete()
        jsonData={
            'message':'Whishlist added successfully'
        }
        return JsonResponse(jsonData)

  
def search(request):
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlist=len(Whishlist.objects.filter(user=request.user))
    query =request.GET['search']
    product=Product.objects.filter(title__icontains=query)
    return render(request,'search.html',locals())