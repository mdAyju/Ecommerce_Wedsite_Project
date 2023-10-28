from django.db import models
from django.contrib.auth.models import User

# Create your models here.


STATUS_CHOICE=(
    ('Accepted','Accepted'),
    ('Pending','Pending'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Cancel','Cancel'),
    ('Deliverd','Delivered')
)

CATEGORY_CHOICE=(
    ('CR','Curd'),
    ('MS','Milkshake'),
    ('ML','Milk'),
    ('LS','Lassi'),
    ('PN','Panner'),
    ('GH','Ghee'),
    ('CZ','Cheese'),
    ('IC','Ice-Cream')
)


STATE_CHOICE=(
('Andhra Pradesh','Andhra Pradesh'),
('Arunachal Pradesh','Arunachal Pradesh'),
('Assam','Assam'),
('Bihar','Bihar'),
('Chhattisgarh','Chhattisgarh'),
('Goa','Goa'),
('Gujarat','Gujarat'),
('Haryana','Haryana'),
('Himachal Pradesh','Himachal Pradesh'),
('Jammu and Kashmir','Jammu and Kashmir'),
('Jharkhand','Jharkhand'),
('Karnataka','Karnataka'),
('Kerala','Kerala'),
('Madhya Pradesh','Madhya Pradesh'),
('Maharashtra','Maharashtra'),
('Manipur','Manipur'),
('Meghalaya','Meghalaya'),
('Mizoram','Mizoram'),
('Nagaland','Nagaland'),
('Odisha','Odisha'),
('Punjab','Punjab'),
('Rajasthan','Rajasthan'),
('Sikkim','Sikkim'),
('Tamil Nadu','Tamil Nadu'),
('Telangana','Telangana'),
('Tripura','Tripura'),
('Uttarakhand','Uttarakhand'),
('Uttar Pradesh','Uttar Pradesh'),
('West Bengal','West Bengal'),
('Andaman and Nicobar Islands','Andaman and Nicobar Islands'),
('Chandigarh','Chandigarh'),
('Dadra and Nagar Haveli','Dadra and Nagar Haveli'),
('Daman and Diu','Daman and Diu'),
('Delhi','Delhi'),
('Lakshadweep','Lakshadweep'),
('Puducherry','Puducherry')
)

class Product(models.Model):
    title=models.CharField(max_length=200)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    description=models.TextField()
    composition=models.TextField()
    prodapp=models.TextField()
    category=models.CharField(choices=CATEGORY_CHOICE,max_length=10)
    product_image=models.ImageField(upload_to='')

    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=22)
    locality=models.TextField(max_length=33)
    city=models.CharField(max_length=33)
    mobile=models.IntegerField(default=0)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICE,max_length=50)

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)


    @property
    def total_cost(self):
        return self.quantity*self.product.discount_price



class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.FloatField()
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status=models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
    paid=models.BooleanField(default=False)



class OrderPlaced(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    Customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity= models.PositiveIntegerField(default=1)
    ordered_date=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=55,choices=STATUS_CHOICE,default='Pending')
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,default='')

    @property
    def total_cost(self):
        return self.quantity*self.product.discount_price

class Whishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)