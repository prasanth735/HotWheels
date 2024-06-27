from django.shortcuts import render

from royaldrive.models import Car,FavouriteItem,Favourites,Order,OrderItems

from api.serializers import FuelSerializer,BrandSerializer,CarSeializer,FavoriteSerializer,FavoriteitemSerializer,orderSerializer

from rest_framework.generics import ListAPIView,RetrieveAPIView,DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication,permissions



import razorpay
# Create your views here.






class IndexapiView(ListAPIView):

    serializer_class=CarSeializer
    queryset=Car.objects.all()



class  CardetailApiView(RetrieveAPIView):

    serializer_class=CarSeializer
    queryset=Car.objects.all()



class AddToFavoriteApiView(APIView):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def post (self,request,*args,**kwargs):

        basket_obj=request.user.cart

        id=kwargs.get("pk")
        car_obj=Car.objects.get(id=id)

        if car_obj in request.user.cart.get_fav_car:
            
            return Response(data={"message" : "car can't add To Favorite"})
        
        else:
            FavouriteItem.objects.create(
                basket_object=basket_obj,
                car_object=car_obj
            )
            return Response(data={"message ": "car added"})
        

class FavoriteCarlistApiView(APIView):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    def get(self,request,*args,**kwargs):

        qs=request.user.cart

        serializer_instance=FavoriteSerializer(qs)

        return Response(data=serializer_instance.data)


    

class FavoriteCarRemoveView(DestroyAPIView):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=FavoriteitemSerializer
    queryset=FavouriteItem.objects.all()



class CheckoutView(APIView):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):
        
        user_obj=request.user
        
        phone=request.data.get("phone")
        email=request.data.get("email")

        order_object=Order.objects.create(
            user_object=user_obj,
            phone=phone,
            email=email,
        )


        basket_items=request.user.cart.cart_items

        for bi in basket_items:
            OrderItems.objects.create(
                order_object=order_object,
                basket_item_object=bi
            )
            bi.is_paid=True
            bi.save()
            # order_object.save()


            # return Response(data={"message":"created"})

        
        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
        data = { "amount": 2000*100, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        print(payment)
        
        order_id=payment.get("id")
        order_total=payment.get("amount")
        user=request.user.username
        data={
            "order_id":order_id,
            "order_total":order_total,
            "user":user,
            "phone":phone
        }
        order_object.order_id=order_id
        order_object.save()
        return Response(data=data,status=status.HTTP_201_CREATED)





class OrderSummaryView(ListAPIView):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    serializer_class=orderSerializer
    queryset=Order.objects.all()


    def get_queryset(self):
        return Order.objects.filter(user_object=self.request.user)

        



class PaymentVerificationView(APIView):


    def post(self,request,*args,**kwargs):

        data=request.data
        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

        try:

            client.utility.verify_payment_signature(data)

            order_id=data.get("razorpay_order_id")

            order_obj=Order.objects.get(order_id=order_id)
            order_obj.is_paid=True
            order_obj.save()

            return Response(data={"message":"payment success"},status=status.HTTP_200_OK)
        except:

            return Response(data={"message":"payment error"},status=status.HTTP_400_BAD_REQUEST)