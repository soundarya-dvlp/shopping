from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path("",views.index,name="index"),
    path("about",views.about,name="about"),
    path("product",views.product,name="product"),
    path("service",views.service,name="service"),
    path("contact",views.contact,name="contact"),
    path("registration",views.registration,name="registration"),
    path("account",views.account,name="account"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("addproduct",views.addproduct,name="addproduct"),
    path("cart",views.cart,name="cart"),
    path("addtocart/<int:id>",views.addtocart,name="addtocart"),
    path("myorder",views.myorder,name="myorder"),
    path("checkout",views.checkout,name="checkout"),
    path("confirmed",views.confirmed,name="confirmed"),
    path("categories",views.categories,name="categories"),

 
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)