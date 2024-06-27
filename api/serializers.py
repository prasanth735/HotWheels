from rest_framework import serializers

from royaldrive.models import Brand,Fuel,Car,FavouriteItem,Favourites,Order,OrderItems

from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):

    password1=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)
    class Meta:

        model=User
        fields=["id","username","email","password1","password2","password"]
        read_only_fields=["id","password"]

    def create(self, validated_data):
        
        password1=validated_data.pop("password1")
        password2=validated_data.pop("password2")

        if password1 != password2:

            raise serializers.ValidationError("password miss match")
        else:

            return User.objects.create_user(**validated_data,password=password1)





class BrandSerializer(serializers.ModelSerializer):

    class Meta:

        model=Brand
        fields=["id","name"]


class FuelSerializer(serializers.ModelSerializer):

    class Meta:

        model=Fuel
        fields=["id","fuel"]


class CarSeializer(serializers.ModelSerializer):

    brand_object=BrandSerializer(read_only=True)
    fuel_type=FuelSerializer(read_only=True)

    class Meta:

        model=Car
        fields="__all__"



class FavoriteCarSerializer(serializers.ModelSerializer):


    class Meta:

        model=Car
        fields=["id","brand_object","name","price"]



class FavoriteitemSerializer(serializers.ModelSerializer):
    car_object=FavoriteCarSerializer(read_only=True)

    class Meta:
        model=FavouriteItem
        fields=["id","car_object","basket_object"]



class FavoriteSerializer(serializers.ModelSerializer):

    owner=serializers.StringRelatedField()
    cart_items=FavoriteitemSerializer(many=True,read_only=True)
    # get_fav_car=serializers.CharField(read_only=True)

    class Meta:
        model=Favourites
        fields=["id","owner","cart_items"]
        






class orderSerializer(serializers.ModelSerializer):
    user_object=serializers.StringRelatedField()
    class Meta:

        model=Order
        fields=["user_object","phone","email","is_paid","order_id","status"]
        

class OrderItemSerializer(serializers.ModelSerializer):

    order_object=orderSerializer()
    basket_item_object=FavoriteCarSerializer()
    ()
  

    class Meta:
        model=OrderItems
        fields="__all__"