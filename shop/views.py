from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .product import Product
from .category import Category
from django.contrib.auth.hashers import make_password,check_password
from .customer import Customer
from django.contrib.auth import logout as logouts
from django.views.decorators.http import require_http_methods
from .orders import Order
from .orderitem import OrderItem
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse



# Create your views here.
def home(request):
    categories=Category.objects.all()
    categoryID=request.GET.get('category')
    if categoryID:
        products=Product.get_category_id(categoryID)
    else:
        products=Product.objects.all()
    data={'products':products,'categories':categories}
    return render(request,'index.html',data)

def signup(request):
    if request.method=='GET':
        return render(request,'signup.html')
    else:
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        mobile=request.POST['mobile']
        email=request.POST['email']
        password=request.POST['password']
        password=make_password(password)
        userdata=[first_name,last_name,mobile,email,password]
        print(userdata)

        #storing object
        customerdata=Customer(first_name=first_name,last_name=last_name,mobile=mobile,email=email,password=password)
        #validation
        error_msg=None
        success_msg=None
        # if(not first_name,last_name,mobile,email,password):
        #     error_msg="Please fill all required fields"
        if(not first_name):
            error_msg="First Name Required !"
        elif(not last_name):
            error_msg="Last Name Required !"
        elif(not mobile):
            error_msg="Mobile Number Required !"
        elif(not email):
            error_msg="Email Required !"
        elif(not password):
            error_msg="Password Required !"
        elif(customerdata.isexist()):
            error_msg='Email Already Exists'
        if (not error_msg):
            success_msg="Account Created Successfully"
            customerdata.save()
        msg={'error':error_msg,'success':success_msg}
        return render(request,'signup.html',msg)


def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    else:
        email=request.POST['email']
        password=request.POST['password']
        #to check email found or not
        users=Customer.getemail(email)
        error_msg=None
        if users:
            check=check_password(password,users.password)
            #if password found
            if check:
                return redirect('/')
            else:
                error_msg='password is incorrect'
                msg={'error':error_msg}
                return render(request,'login.html',msg)
        else:
            error_msg='email is incorrect'
            msg={'error':error_msg}
            return render(request,'login.html',msg)

def logout(request):
    if request.method=='POST':
        logouts(request)
        return redirect('home')
    else:
        return render(request,'logout.html')


# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'index.html', {'products': products})

def cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    total = 0
    cart_items = []
    for product in products:
        item = {
            'product': product,
            'quantity': cart[str(product.id)]['quantity'],
            'subtotal': product.price * cart[str(product.id)]['quantity']
        }
        cart_items.append(item)
        total += item['subtotal']

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product = Product.objects.get(id=product_id)
    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {'price': str(product.price), 'quantity': 1}
    request.session['cart'] = cart
    return redirect('cart')



def update_cart(request):
    cart = request.session.get('cart', {})

    if request.method == "POST":
        # Handling the update
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                quantity = int(value)
                if product_id in cart and quantity > 0:
                    cart[product_id]['quantity'] = quantity
                elif product_id in cart and quantity == 0:
                    del cart[product_id]

        # Handling the remove button
        if 'remove' in request.POST:
            product_id = request.POST['remove']
            if product_id in cart:
                del cart[product_id]

        request.session['cart'] = cart
        return HttpResponseRedirect(reverse('cart'))

    return HttpResponseRedirect(reverse('cart'))
