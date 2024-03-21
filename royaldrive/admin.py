from django.contrib import admin
from royaldrive.models import Brand,Car,Fuel,favouriteItem,favourites

# Register your models here.


admin.site.register(Brand)
admin.site.register(Car)
admin.site.register(Fuel)
admin.site.register(favouriteItem)
admin.site.register(favourites)
