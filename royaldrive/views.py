from django.shortcuts import render,redirect
from django.views.generic import View
from royaldrive.forms import RegistrationForm,SigninForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from royaldrive.models import Car

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


class IndexView(View):
    def get(self,request,*args,**kwargs):
        qs=Car.objects.all()
        return render (request,"index.html",{"data":qs})


class DeatilView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Car.objects.get(id=id)
        return render(request,"detail.html",{"data":qs})






