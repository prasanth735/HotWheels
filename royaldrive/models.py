from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


# Create your models here.
class Brand(models.Model):
    name=models.CharField(max_length=200,unique=True,) 
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name  
    
    
class Fuel(models.Model):
    fuel=models.CharField(max_length=200) 
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)


    def __str__(self):
        return self.fuel
    

class Car(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField(null=True)
    brand_object=models.ForeignKey(Brand,on_delete=models.DO_NOTHING)
    price=models.PositiveIntegerField()
    year=models.PositiveIntegerField()
    image=models.ImageField(upload_to="car_images",default="default.jpg",blank=True,null=True)
    registered_state=models.CharField(max_length=200)
    distance_travelled=models.PositiveIntegerField()
    fuel_type=models.ForeignKey(Fuel,on_delete=models.DO_NOTHING)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    is_sold=models.BooleanField(default=False)

    def __str__(self):
        return self.name  


class Favourites(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)

    @property
    def cart_items(self):
        return self.cartitem.filter(is_item_booked=False)
    


    @property
    def get_fav_car(self):
        car=[c.car_object for c in FavouriteItem.objects.all()]

        return car

class FavouriteItem(models.Model):
    car_object=models.ForeignKey(Car,on_delete=models.CASCADE)
    basket_object=models.ForeignKey(Favourites,on_delete=models.CASCADE,related_name="cartitem")
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=True)
    is_item_booked=models.BooleanField(default=False)

    @property
    def car_stat(self):

        return self.car_object




def create_basket(sender,instance,created,**kwargs):
    if created:
        Favourites.objects.create(owner=instance)

post_save.connect(create_basket,sender=User)



class Order(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="purchase")
    phone=models.CharField(max_length=12)
    email=models.CharField(max_length=200,null=True)
    is_paid=models.BooleanField(default=False)
    order_id=models.CharField(max_length=200,null=True)
    option=(
        ("booked","booked"),
        ("delivered","delivered"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=200,choices=option,default="booked")

    @property
    def get_order_items(self):
        return self.purchaseitems.all()    



class OrderItems(models.Model):
    order_object=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="purchaseitems")
    basket_item_object=models.ForeignKey(FavouriteItem,on_delete=models.CASCADE)
