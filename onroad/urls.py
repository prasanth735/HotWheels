"""
URL configuration for onroad project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from royaldrive import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup',views.SignupView.as_view(),name="signup"),
    path('',views.SigninView.as_view(),name="signin"),
    path('index',views.IndexView.as_view(),name="index"),
    path('detail/<int:pk>/',views.DeatilView.as_view(),name="detail"),
    path('car/<int:pk>/addtofavorite',views.AddtofavoriteView.as_view(),name="favorite"),
    path('car/favorite',views.FavoriteListView.as_view(),name="favorite-list"),
    path('car/<int:pk>/delete',views.FavoriteremoveView.as_view(),name="favorite-remove"),
    path("checkout/",views.CheckoutView.as_view(),name="checkout"),
    path("payment/verification",views.PaymentVerificationView.as_view(),name="verification"),
    path("summary/",views.Order_summaryView.as_view(),name="summary"),
    path("logout/",views.Logoutview.as_view(),name="logout"),
    # path("directcheckout/",views.DirectCheckoutView.as_view(),name="directbook"),



    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
