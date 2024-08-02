from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .models import Contact,Registration,Product,Cart,Order,Category

# Create your views here.
def index(request):
    cat=Category.objects.all().values()
    context ={
        'cat':cat
    } 
    template=loader.get_template("index.html")
    return HttpResponse(template.render(context,request))

def about(request):
    template=loader.get_template("about.html")
    return HttpResponse(template.render({},request))


def service(request):
    template=loader.get_template("service.html")
    return HttpResponse(template.render({},request))
def contact(request):
    if request.method == 'POST':
        cname=request.POST["contact_name"]
        cemail=request.POST["contact_email"]
        cmessage=request.POST["contact_message"]
        con=Contact(
            con_name=cname,
            con_email=cemail,
            con_message=cmessage,
        )
        con.save()
    template=loader.get_template("contact.html")
    return HttpResponse(template.render({},request))

def registration(request):
    if 'usersession' in request.session:
        return HttpResponseRedirect('/account')
    if 'registration_name' in request.POST:
        rname=request.POST["registration_name"]
        remail=request.POST["registration_email"]
        rnumber=request.POST["registration_phonenumber"]
        rusername=request.POST["registration_username"]
        rpassword=request.POST["registration_password"]
        reg=Registration(
            reg_name=rname,
            reg_email=remail,
            reg_number=rnumber,
            reg_username=rusername,
            reg_password=rpassword,
        )
        reg.save()
    template=loader.get_template("registration.html")
    return HttpResponse(template.render({},request))

def login(request):
    if "usersession" in request.session:
        return HttpResponseRedirect('/account')
    if request.method == "POST":
        log_id=request.POST['log_id']
        log_pswd=request.POST['log_pswd']

        login=Registration.objects.filter(
            reg_username=log_id,
            reg_password=log_pswd
        )
        
        if login:
            request.session['usersession']=log_id
            return HttpResponseRedirect('/account')
        else: 
            return HttpResponseRedirect('/registration')
    template=loader.get_template("login.html")
    return HttpResponse(template.render({},request))
   
def account(request):
    if "usersession" not in request.session:
        return HttpResponseRedirect('/login')
    
    template=loader.get_template("account.html")
    return HttpResponse(template.render({},request))

def logout(request):
    if 'usersession' in request.session:
        del request.session['usersession']
        return HttpResponseRedirect("/login")
    
def addproduct(request):
    if request.method =='POST':
        pro_name  =  request.POST['pro_name']
        pro_price = request.POST["pro_price"]
        pro_image = request.FILES["pro_image"]
        pro_catid = request.POST["pro_catid"]

        product= Product(
            pro_name=pro_name,
            pro_price=pro_price,
            pro_image=pro_image, 
            pro_catid=pro_catid, 

        )
        product.save()
    cat=Category.objects.all().values()
    context ={
        'cat':cat
    } 
    template=loader.get_template("addproduct.html")
    return HttpResponse(template.render(context,request))

def product(request):
    if 'catid' in request.GET:
        catid=request.GET['catid']
        products=Product.objects.filter(pro_catid=catid)
    else:
        products=Product.objects.all().values()

    context={
        'products':products
    }
    template =loader.get_template("product.html")
    return HttpResponse(template.render(context,request))
def addtocart(request,id):
    if 'usersession' not in request.session:
        return HttpResponseRedirect("/login")


    exist=Cart.objects.filter(cart_proid=id,cart_user=request.session["usersession"])
    if exist:
        exstcart= Cart.objects.filter(cart_proid=id,cart_user=request.session["usersession"])[0]
        exstcart.cart_qty+=1
        exstcart.cart_amount=exstcart.cart_qty* exstcart.cart_price
        exstcart.save()
    else:
        pro= Product.objects.filter(id=id)[0]

        cart= Cart(cart_user=request.session["usersession"],
              cart_proid=pro.id,
              cart_name=pro.pro_name,
              cart_price=pro.pro_price,
              cart_image=pro.pro_image,
              cart_qty=1,
              cart_amount=pro.pro_price)
                   
        cart.save()
    return HttpResponseRedirect('/cart')
def cart(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
        
    if 'del' in request.GET:
        id=request.GET['del']
        delcart=Cart.objects.filter(id=id)[0]
        delcart.delete()
    if 'q' in request.GET:
        q=request.GET ['q']
        cp=request.GET['cp']
        cart3=Cart.objects.filter(id=cp)[0]

        if q=='inc':
            cart3.cart_qty+=1
        elif q=='dec':
            if(cart3.cart_qty>1):
                cart3.cart_qty-=1
        cart3.cart_amount=cart3.cart_qty * cart3.cart_price
        cart3.save()

    user=request.session["usersession"]
    cart2=Cart.objects.filter(cart_user=user)

    tot=0 
    shp=0 
    gst=0 
    gtot=0
    for x in cart2:
        tot=+x.cart_amount

        shp=tot *10/100
        gst=tot *18/100
        gtot=tot+shp+gst

        request.session["tot"]=tot
        request.session["gst"]=gst
        request.session["shp"]=shp
        request.session["gtot"]=gtot
    cart=Cart.objects.filter(cart_user=user).values()
    context={
        'cart':cart,
        'tot' :tot,
        'shp':shp,
        'gst':gst,
        'gtot':gtot
    }


    template=loader.get_template("cart.html")
    return HttpResponse(template.render(context,request))
def myorder(request):
    user=request.session["usersession"]
    order= Order.objects.filter(order_user=user,order_status=1)
    context={
        'order':order
    }
    template=loader.get_template("myorder.html")
    return HttpResponse(template.render(context,request))
def checkout(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect('/login')
    co =0
    adrs = dtype=""
    if 'dlv_adrs' in request.POST:
        adrs=request.POST["dlv_adrs"]
        dtype=request.POST["dlv_type"]
        co=1
        
    user=request.session["usersession"]
    oldodr=Order.objects.filter(order_user=user,order_status=0)
    oldodr.delete()
    cart=Cart.objects.filter(cart_user=user)
    for x in cart:
        odr=Order(order_user=user,
                  order_name=x.cart_name,
                  order_image=x.cart_image,
                  order_price=x.cart_price,
                  order_qty=x.cart_amount,
                  order_address=adrs,
                  order_dlptyp=dtype,
                  order_status=0)
        odr.save()
    order=Order.objects.filter(order_user=user,order_status=0).values()
    tot=request.session["tot"]
    gst=request.session["gst"]
    shp=request.session["shp"]
    gtot=request.session["gtot"]
    context={

        'order':order,
        'tot':tot,
        'shp':shp,
        'gst':gst,
        'gtot':gtot,
        'co':co
        }

    template=loader.get_template("checkout.html")
    return HttpResponse(template.render(context,request))
def confirmed(request):
    if 'usersession' not in request.session:
        return HttpResponseRedirect("/login")
    user=request.session["usersession"]
    order=Order.objects.filter(order_user=user,order_status=0)
    for x in order:
        x.order_status=1
        x.save()
    template=loader.get_template("confirmed.html")
    return HttpResponse(template.render({},request))

def categories(request):
    if request.method =='POST':
        cat_name  =  request.POST['cat_name']
        cat_image = request.FILES["cat_image"]

        cat= Category(
            cat_name=cat_name,
            cat_image=cat_image,

        )
        cat.save()
    
    template=loader.get_template("addcategories.html")
    return HttpResponse(template.render({},request))