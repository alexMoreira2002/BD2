from django.shortcuts import render, redirect
from ..database.cart import *
from ..database.products import *


def listCart(request):
    page = "cart.html"
    context = {}
    if request.method == 'GET':
        token = request.session.get('login_token')
        if token is not None:
            page = "cart.html"
            userId = request.session.get('user_id')
            print(userId)
            cartList = list(getCartByUserMongoDB(userId))
            productCount = {}
            cartListProducts = []
            for cartItem in cartList:
                product_id = cartItem['productID']
                cartID = cartItem['_id']
                str = getProductMongoDB(product_id)
                cartListProducts.append({'cartID': cartID, 'productName': str['productName'], 'productImage': str['productImage'], 'productPriceStart': str[
                                        'productPriceStart'], 'productPriceEnd': str['productPriceEnd'], 'id': str['_id'], 'productDescription': str['productDescription'], })
            #print(productCount)
            #print(cartListProducts)
            context = {'productCount': productCount,
                       'cartListProducts': cartListProducts, 'userID':userId}
        else:
            return redirect('login')
    return render(request, page, context=context)


def addCart(request):
    page = "cart.html"
    context = {}
    if request.method == 'POST':
        token = request.session.get('login_token')
        if token is not None:
            page = "cart.html"
            productID = request.GET.get('id')
            userId = request.session.get('user_id')
            result = addProductToCart(userId, productID)
            if result:
                print('Product added to cart successfully')
                return redirect('cart')
        else:
            return redirect('login')
    return render(request, page, context=context)


def removeCart(request):
    page = "cart.html"
    context = {}
    if request.method == 'POST':
        token = request.session.get('login_token')
        if token is not None:
            page = "cart.html"
            cartID = request.GET.get('id')
            print(cartID)
            result = removeProductFromCart(cartID)
            if result == True:
                print('Product removed from cart successfully')
                page = "cart.html"
        else:
            return redirect('login')
    return render(request, page, context=context)
