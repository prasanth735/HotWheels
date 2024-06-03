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

