from django.contrib import admin
from royaldrive.models import Brand,Car,Fuel,FavouriteItem,Favourites,Order,OrderItems

# Register your models here.


admin.site.register(Brand)
admin.site.register(Car)
admin.site.register(Fuel)
admin.site.register(FavouriteItem)
admin.site.register(Favourites)
admin.site.register(Order)
admin.site.register(OrderItems)
