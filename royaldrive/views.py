KEY_ID=""
KEY_SECRET=""


from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache


from royaldrive.forms import RegistrationForm,SigninForm
from royaldrive.models import Car,FavouriteItem,Favourites,Order,OrderItems
from royaldrive.decorators import SigninRequired

import razorpay

# Create your views here.


class SignupView(View):
    
    def get(self,request,*args,**kwargs):
        form=RegistrationForm
        return render (request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        return render (request,"login.html",{"form":form})
    

class SigninView(View):

    def get(self,request,*args,**kwargs):
        form=SigninForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=SigninForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                login(request,user_object)
                return redirect("index")
        messages.error(request,"invalid credential")
        return render(request,"login.html",{"form":form})

@method_decorator([SigninRequired,never_cache],name="dispatch")
class IndexView(View):

    def get(self,request,*args,**kwargs):
        qs=Car.objects.all()
        return render (request,"index.html",{"data":qs})

@method_decorator([SigninRequired,never_cache],name="dispatch")
class DeatilView(View):

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Car.objects.get(id=id)
        return render(request,"detail.html",{"data":qs})

@method_decorator([SigninRequired,never_cache],name="dispatch")
class AddtofavoriteView(View):

    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        car_obj=Car.objects.get(id=id)

        # fav_cars=[ c for c in request.user.cart.cartitem.get_fav_items]


        # if car_obj in fav_cars:

        #     messages.error(request,"car already exist")
        #     return redirect("index")
        # else:

        FavouriteItem.objects.create(
            car_object=car_obj,
            basket_object=request.user.cart
        )
        return redirect("favorite-list")
        

@method_decorator([SigninRequired,never_cache],name="dispatch")
class FavoriteListView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.cart.cartitem.filter(is_item_booked=False)
        return render(request,"favorites.html",{"data":qs})
    

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        # car_obj=request.user.cart.cartitem.get(id=id)
        print(kwargs,id)
        return render(request,"checkout.html")


@method_decorator([SigninRequired,never_cache],name="dispatch")
class FavoriteremoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        FavouriteItem.objects.get(id=id).delete()
        return redirect ("favorite-list")
    
@method_decorator([SigninRequired],name="dispatch")
class CheckoutView(View):
    
    def get(self,request,*args,**kwargs):

        return render(request,"checkout.html")


    def post(self,request,*args,**kwargs):

        email=request.POST.get("email")
        phone=request.POST.get("phone")


        order_obj=Order.objects.create(
            user_object=request.user,
            phone=phone,
            email=email,
        )
        try:
            favorite_items=request.user.cart.cart_items


            for bi in favorite_items:
                OrderItems.objects.create(
                    order_object=order_obj,
                    basket_item_object=bi
                )
                bi.is_item_booked=True
                bi.car_object.is_sold=True
                bi.save()

        except:
            order_obj.delete()


        finally:

            client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
            data = { "amount": 2000*100, "currency": "INR", "receipt": "order_rcptid_11" }
            payment = client.order.create(data=data)
            order_obj.order_id=payment.get("id")
            order_obj.save()
            print(payment)
            context={
                "key":KEY_ID,
                "order_id":payment.get("id"),
                "amount":payment.get("amount")
            }
            return render(request,"payment.html",{"context":context})
        
    
            
@method_decorator(csrf_exempt,name="dispatch")
class PaymentVerificationView(View):

    def post(self,request,*args,**kwargs):
        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
        data=request.POST

        try:
            client.utility.verify_payment_signature(data)
            print(data)
            order_obj=Order.objects.get(order_id=data.get("razorpay_order_id"))
            order_obj.is_paid=True
            order_obj.save()

            print("******************************transaction complete *******************")
            return render(request,"success.html")


        except:
            print("!!!!!!!!!!!!!!!!!!!!!transaction failed==================================")

            return redirect("signin")

    

@method_decorator([SigninRequired,never_cache],name="dispatch")
class Logoutview(View):
     
    def get(self,request,*args,**kwargs):

        logout(request)
        return redirect("signin")
    

@method_decorator([SigninRequired,never_cache],name="dispatch")
class Order_summaryView(View):

    def get(self,request,*args,**kwargs):
        qs=Order.objects.filter(user_object=request.user).exclude(status="cancelled")
        return render (request,"summary1.html",{"data":qs})
    



