

from django.urls import path

from api.views import IndexapiView,CardetailApiView,AddToFavoriteApiView,FavoriteCarlistApiView
from api import views
urlpatterns=[

    path("cars",IndexapiView.as_view()),
    path("<int:pk>/cars",CardetailApiView.as_view()),
    path("<int:pk>/addtofavorite",AddToFavoriteApiView.as_view()),
    path("favoritelist",FavoriteCarlistApiView.as_view()),
    path("favorite/remove/<int:pk>",views.FavoriteCarRemoveView.as_view()),
    path("order",views.CheckoutView.as_view()),
    path('payment/verification/',views.PaymentVerificationView.as_view()),
    path("summary",views.OrderSummaryView.as_view())


]