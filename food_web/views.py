from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product, Cart, Person, Feedback, Store, Order
from django.db.models import Q

# Create your views here.

def register(request):
    context = {}
    if request.method == 'POST':
        fn = request.POST['fname']
        ln = request.POST['lname']
        em = request.POST['email']
        pw = request.POST['password']
        cpw = request.POST['confirm_password']
        mob = request.POST.get('mobile','')
        add = request.POST.get('address','')
        print(fn, ln, em, pw, cpw)

        if fn == "" or ln == "" or em == "" or pw == "" or cpw == "":
            context["errmsg"] = "Fiels cannot be empty."
            return render(request,'register.html',context)
        elif pw != cpw:
            context["errmsg"] = "Password does not match."
            return render(request,'register.html',context)
        elif not (any(c.isupper() for c in pw) and
                any(c.isdigit() for c in pw) and
                any(c in "!@#$&*" for c in pw)):
            context["errmsg"] = "Password must contain atleast 1 uppercase letter, 1 special symbol, 1 number."
            return render(request,'register.html',context)
        elif len(pw) < 8:
            context["errmsg"] = "Password must be atleast 8 characters long."
            return render(request,'register.html',context)
        elif User.objects.filter(email = em).exists():
            context["errmsg"] = "User already registered."
            return render(request,'register.html',context)
        else:
            u = User.objects.create(first_name=fn , last_name=ln, username=em, email=em)
            u.set_password(pw)
            u.save()

            p = Person.objects.create(user_id=u , mobile=mob, address=add)
            p.save()
            return redirect('/dashboard')
        
    return render(request, 'register.html')


def ulogin(request):
    context = {}
    if request.method == 'POST':
        em = request.POST['email']
        pw = request.POST['password']
        print(em, pw)

        u = authenticate(username=em,password=pw)     #used to check if username and password is authenticated or not. To authenticate, password must be hash protected.
        print(u)

        if u is not None:
            login(request, u)                          #start the session and stores id of authenticated user from auth_user in session
            return redirect('/dashboard')
        else:
            context["errmsg"] = "Password does not match."
            return render(request, 'login.html',context)
                
    return render(request, 'login.html',context)

def ulogout(request):
    print("User: ", request.user, "Logged out")
    logout(request)
    return redirect('/login')

def dashboard(request):
    print("ID of Logged in User: ", request.user.id)                              #To check which user is logged in
    context = {}
    u = User.objects.filter(id = request.user.id)
    context['data'] = u
    p = Product.objects.order_by('?')[:3]
    context['products'] = p
    a = Product.objects.filter(is_active=True).order_by('-id')[:3]
    context['new'] = a
    return render(request, 'dashboard.html', context)

def menu(request):
    context = {}
    query = request.GET.get('q')
    u = User.objects.filter(id = request.user.id)
    context['data'] = u
    p = Product.objects.all()
    if query:
        p = p.filter(name__icontains = query)
    context['products'] = p
    return render(request, 'menu.html', context)

def cat_filter(request, cid):
    p = Product.objects.filter(cat = cid)
    context = {}
    context['products'] = p
    
    return render(request, 'menu.html', context)

def price_sort(request, sid):
    if sid == "high_to_low":
        p = Product.objects.order_by("-price").filter(is_active=True)
    else:
        p = Product.objects.order_by("price").filter(is_active=True)

    context = {}
    context['products'] = p

    return render(request, 'menu.html', context)

def profile(request):
    context = {}
    u = Person.objects.filter(user_id = request.user.id)
    context['data'] = u
    return render(request, 'profile.html', context)

def details(request, pid):
    p = Product.objects.filter(id = pid)
    context = {}
    context['data'] = p
    return render(request, 'product_details.html', context)

def cart(request):
    context = {}
    u = User.objects.filter(id = request.user.id)
    context['data'] = u
    c = Cart.objects.filter(user_id = request.user.id)
    context['carts'] = c
    sum = 0
    q1 = 0
    for i in c:
        sum = sum + i.pid.price*i.Qty
        q1 += i.Qty
    
    tax = sum * 0.09
    total = sum + tax + tax
    context['price'] = sum
    context['quantity'] = q1
    context['tax'] = "{:.2f}".format(tax)
    context['amount'] = "{:.2f}".format(total)
    return render(request, 'cart.html', context)

def addtocart(request, aid):
    context= {}
    if request.user.is_authenticated:
        u = User.objects.filter(id = request.user.id)
        p = Product.objects.filter(id = aid)
        context['data'] = p
        q1 = Q(user_id = u[0])
        q2 = Q(pid = p[0])
        c = Cart.objects.filter(q1 & q2)
        n = len(c)
        if n == 1:
            context['msg'] = "Item already exist in the cart."
            return render(request, 'product_details.html', context)
        else:
            c = Cart.objects.create(pid=p[0], user_id=u[0])
            c.save()
            context['msg'] = "Item added in the cart."       
            return render(request, 'product_details.html', context)
    else:
        return redirect('/login')
    
def update_qty(request, x, qid):
    c = Cart.objects.filter(id = qid)
    q = c[0].Qty
    if x == "1":
        q += 1
    elif q > 1:
        q -= 1
    c.update(Qty = q)
    return redirect('/cart')

def editprofile(request, eid):
    context = {}
    if request.method == "GET":    
        u = Person.objects.filter(user_id = eid)
        context['data'] = u
        return render(request, 'editprofile.html', context)
    else:
        mob = request.POST['mobile']
        add = request.POST['address']

        u = Person.objects.filter(user_id = eid)        
        u.update(mobile=mob, address=add)
        return redirect('/profile')

def deleteprofile(request, did):
    u = User.objects.filter(id = did)
    u.delete()

    return redirect('/feedback')

def deleteitem(request, bid):
    c = Cart.objects.filter(id = bid)
    c.delete()
    return redirect('/cart')

def feedback(request):
    context = {}
    if request.method == "POST":
        fn = request.POST['name']
        mob = request.POST['mobile']
        em = request.POST['email']
        fb = request.POST['feedback']

        u = Feedback.objects.create(name=fn, mobile=mob, email=em, feedback=fb)
        u.save()

        context['msg'] = "Thank you for your valuable feedback!"
        return render(request, 'feedback.html', context)
    return render(request, 'feedback.html')

def store(request):
    context = {}
    s = Store.objects.all()
    context['store'] = s
    u = User.objects.filter(id = request.user.id)
    context['data'] = u 
    return render(request, 'store.html', context)

def contact(request):
    context = {}
    u = User.objects.filter(id = request.user.id)
    context['data'] = u 
    return render(request, 'contact.html', context)

def about(request):
    context = {}
    u = User.objects.filter(id = request.user.id)
    context['data'] = u 
    return render(request, 'about.html', context)

import random
def placeorder(request):
    c = Cart.objects.filter(user_id = request.user.id)
    o_id = random.randrange(1000,9999)
    for i in c:
        amt = i.Qty * i.pid.price
        o = Order.objects.create(order_id = o_id, qty = i.Qty, amount = amt, pid = i.pid, user_id = request.user)
        o.save()
        i.delete()
    return redirect('/fetchorder')

def fetchorder(request):
    o = Order.objects.filter(user_id=request.user.id)
    context = {}
    context['orders'] = o
    u = User.objects.filter(id = request.user.id)
    context['data'] = u
    sum = 0
    for i in o:
        sum += i.amount
        #i.delete()

    tax = sum * 0.09
    total = sum + tax + tax
    context['price'] = sum
    context['tax'] = "{:.2f}".format(tax)
    context['amount'] = "{:.2f}".format(total)
    context['price'] = sum
    context['n'] = len(o)

    return render(request, 'placeorder.html', context)

import razorpay
def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_NMRA7qyGBTM6Ei", "LBGZrdTVudukqiu52AwiaQCd"))
    orders=Order.objects.filter(user_id=request.user.id)
    context={}
    context["orders"]=orders
    sum=0
    
    for x in orders:
        sum=sum+x.amount
        orderid=x.order_id
    
    tax = sum * 0.09
    total = sum + tax + tax
    
    data = { "amount": total*100, "currency": "INR", "receipt": orderid }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context["payment"]=payment

    return render(request, 'pay.html',context)