from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Customer, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, LoginForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        return render(request, 'app/home.html',
                      {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles, 'laptops': laptops})


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html',
                      {'product': product, 'item_already_in_cart': item_already_in_cart})


def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        return redirect('showcart')
    else:
        return redirect('login')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 50.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temp = (p.quantity * p.product.discounted_price)
            amount += temp

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 50.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temp = (p.quantity * p.product.discounted_price)
            amount += temp
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temp = (p.quantity * p.product.discounted_price)
            amount += temp
        if amount == 0:
            shipping_amount = 0
        else:
            shipping_amount = 50.0
        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 50.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        total_products = len(cart_product)
        if cart_product:
            for p in cart_product:
                temp = (p.quantity * p.product.discounted_price)
                amount += temp
                total_amount = amount + shipping_amount
            return render(request, 'app/cart.html', {'carts': cart, 'total_amount': total_amount, 'amount': amount,
                                                     'total_products': total_products})
        else:
            return render(request, 'app/emptycart.html')


class ProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = CustomerProfileForm()
            return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
        else:
            return redirect('login')

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile updated Successfully ! ')
            form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


def address(request):
    if request.user.is_authenticated:
        add = Customer.objects.filter(user=request.user)
        return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})
    else:
        return redirect('login')


def delete_address(request, id):
    if request.method == 'POST':
        pi = Customer.objects.get(pk=id)
        pi.delete()
        return redirect('address')


def orders(request):
    if request.user.is_authenticated:
        op = OrderPlaced.objects.filter(user=request.user)
        list_of_op = list(op)
        return render(request, 'app/orders.html', {'order_placed': list_of_op[::-1]})
    else:
        return redirect('login')


def mobile(request, data=None):
    if data is None:
        mobiles = Product.objects.filter(category='M')
    else:
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    return render(request, 'app/mobile.html', {'mobiles': mobiles})


def laptop(request, data=None):
    if data is None:
        laptops = Product.objects.filter(category='L')
    else:
        laptops = Product.objects.filter(category='L').filter(brand=data)
    return render(request, 'app/laptop.html', {'laptops': laptops})


def topwear(request):
    topwears = Product.objects.filter(category='TW')
    return render(request, 'app/topwear.html', {'topwears': topwears})


def bottomwear(request):
    bottomwears = Product.objects.filter(category='BW')
    return render(request, 'app/bottomwear.html', {'bottomwears': bottomwears})


def loginview(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    return redirect('profile')
        else:
            form = LoginForm()
        return render(request, 'app/login.html', {'form': form})
    else:
        return redirect('profile')


def customerregistration(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account created successfully !')
            form.save()
            form = CustomerRegistrationForm()
    else:
        form = CustomerRegistrationForm()
    return render(request, 'app/customerregistration.html', {'form': form})


def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 50.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            temp = (p.quantity * p.product.discounted_price)
            amount += temp
        total_amount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add': add, 'totalamount': total_amount, 'cart_items': cart_items})


def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')
