from django.shortcuts import render, redirect
from ..database.orders import *
from ..database.products import *
from ..database.users import *
from ..database.cart import *


def createOrder(request):
    context = {}
    if request.method == 'POST':
        userId = request.session.get('user_id')
        if userId is not None:
            productID = request.GET.get('id')
            cartID = request.GET.get('idCart')
            userIDCart = request.GET.get('userID')
            if cartID is not None:
                cart = getCartMongoDB(cartID)
                productList = []
                productPrice = []
                productIDCart = cart['productID']
                productList.append(str(productIDCart))
                product = getProductMongoDB(productIDCart)
                productPriceAux = str(product['productPriceEnd'])
                productPrice.append(productPriceAux)

                result = insertOrder(productList, userId, productPrice)
                quantity = product['productQuantity']
                newquantity = int(quantity)-1
                updateProductQuantity(productIDCart, newquantity)
                if newquantity == 0:
                    updateProductStatus(productIDCart)

                if result == True:
                    removeProductFromCart(cartID)
            elif userIDCart is not None:
                cartList = list(getCartByUserMongoDB(userId))
                productList = []
                productPrice = []
                for cartItem in cartList:
                    product_id = cartItem['productID']
                    product = getProductMongoDB(product_id)
                    productPriceAux = str(product['productPriceEnd'])
                    productList.append(str(product_id))
                    productPrice.append(productPriceAux)

                result = insertOrder(productList, userId, productPrice)

                for product in productList:
                    productDetails = getProductMongoDB(product)
                    quantity = productDetails['productQuantity']
                    newquantity = int(quantity)-1
                    updateProductQuantity(product, newquantity)
                    if newquantity == 0:
                        updateProductStatus(productIDCart)

                    if result == True:
                        removeallProductsFromUserCart(userId)
            else:
                product = getProductMongoDB(productID)
                productList = []
                productPrice = []
                productList.append(str(productID))
                productPriceAux = str(product['productPriceEnd'])
                productPrice.append(productPriceAux)
                result = insertOrder(productList, userId, productPrice)
                quantity = product['productQuantity']
                newquantity = int(quantity)-1
                updateProductQuantity(productID, newquantity)
                if newquantity == 0:
                    updateProductStatus(productID)
        else:
            return redirect('login')
    return render(request, "index.html", context=context)


def beforeCreateOrder(request):
    context = {}
    if request.method == 'GET':
        userId = request.session.get('user_id')
        if userId is not None:
            userIDCart = request.GET.get('idUser')
            cartID = request.GET.get('idCart')
            if cartID is not None:
                cart = getCartMongoDB(cartID)
                product = []
                productID = cart['productID']
                product.append(getProductMongoDB(productID))
                context = {'product': product, 'idCart': cartID}
            elif userIDCart is not None:
                cartList = list(getCartByUserMongoDB(userId))
                product = []
                for cartItem in cartList:
                    product_id = cartItem['productID']
                    product.append(getProductMongoDB(product_id))
                context = {'product': product, 'userID': userIDCart}
            else:
                product = []
                productID = request.GET.get('id')
                product.append(getProductMongoDB(productID))
                context = {'product': product, 'id': productID}
        else:
            return redirect('login')

    return render(request, 'addOrder.html', context=context)


def listOrders(request):
    page = 'listOrders.html'
    context = {}
    if request.method == 'GET':
        token = request.session.get('login_token')
        if token is not None:
            page = 'listOrders.html'
            userId = request.session.get('user_id')
            print(userId)
            orders = list(getOrdersByCustomer(userId))
            ordersList = []
            for element in orders:
                for character in element:
                    data = character.split(',')
                    orderID = data[0].strip("()")
                    date = data[2]
                    orderTotal = data[3]
                    quantity = data[4]
                    status = data[5].strip(")")
                ordersList.append(
                    {'orderID': orderID, 'date': date, 'OrderTotal': orderTotal, 'quantity': quantity, 'status': status})
            context = {'ordersList': ordersList}
    return render(request, page, context=context)


def orderDetail(request):
    page = 'orderDetail.html'
    context = {}
    if request.method == 'GET':
        token = request.session.get('login_token')
        if token is not None:
            page = 'orderDetail.html'
            orderID = request.GET.get('id')
            orders = list(getOrder(orderID))
            orderList = []
            for element in orders:
                for character in element:
                    print("character", character)
                    data = character.split(',')
                    orderID = data[0].strip("()")
                    customerID = data[1]
                    date = data[2]
                    orderTotal = data[3]
                    status = data[4]
                    productID = data[5]
                    productPrice = data[6].strip(")")
                    customer = getUserByID(customerID)
                    customerName = customer['name']
                    product = getProductMongoDB(productID)
                    vendorRole = product['roleVendor']
                    if vendorRole == "XPTO":
                        vendorName = vendorRole
                    elif vendorRole == "parceiro":
                        vendorID = product['vendor']
                        vendorProfile = getUserByID(vendorID)
                        vendorName = vendorProfile['name']
                    productName = product['productName']

                    orderList.append(
                        {'productName': productName, 'productPrice': productPrice, 'vendorName': vendorName})

            context = {'orderList': orderList, 'customerName': customerName, 'orderTotal': orderTotal,
                       'orderID': orderID, 'date': date, 'status': status, }
    return render(request, page, context=context)


def getAllOrdersView(request):
    if request.method == 'GET':
        token = request.session.get('login_token')
        if token is not None:
            orders = []
            orders.append(list(getAllOrders()))

            ordersList = []
            for element in orders:
                for character in element:
                    orderID = character[0]
                    productID = character[7]
                    total = str(character[3]).strip("Decimal(' ')")
                    product = getProductMongoDB(productID)
                    ordersList.append(
                        {'orderID': orderID, 'product': product, 'total': total})

    return render(request, 'getAllOrders.html', {'ordersList': ordersList})


def getAllOrdersByUser(request):
    if request.method == 'GET':
        token = request.session.get('login_token')
        if token is not None:
            orders = []
            orders.append(list(getUsersOrdersAndHowMany()))

            ordersList = []
            for element in orders:
                for character in element:
                    data = str(character).split(',')
                    count = data[0].strip("( '( ))")
                    productID = data[2].strip(" '' ) ")
                    customerID = data[1].strip(" ' ")
                    product = getProductMongoDB(productID)
                    customer = getUserByID(customerID)
                    ordersList.append(
                        {'count': count, 'customer': customer, 'product': product})

    return render(request, 'getAllOrdersByUser.html', {'ordersList': ordersList})


def ordersRequests(request):
    if request.method == 'GET':
        ordersList = []
        ordersFalse = []
        ordersFalse.append(getOrderStatusFalse())
        for element in ordersFalse:
            for character in element:
                data = str(character).split(',')

                orderID = data[0].strip("()")

                customerID = data[1].strip(" ' ")

                year = data[2].replace("datetime.date(", "")
                month = data[3]
                day = data[4].strip(")")
                dateNotFinished = str(year)+"-"+str(month)+"-"+str(day)
                date = dateNotFinished.replace("- ", "-")

                orderTotalToStrip = data[5].replace("Decimal('", "")
                orderTotal = orderTotalToStrip.replace("')", "")

                quantity = data[6]

                status = data[7].strip(")")

                customer = getUserByID(customerID)
                customerName = customer['name']

                ordersList.append({'orderID': orderID, 'customerName': customerName, 'orderTotal': orderTotal,
                                   'date': date, 'quantity': quantity})

    return render(request, 'ordersRequests.html', {'ordersList': ordersList})


def acceptOrders(request):
    if request.method == 'POST':
        orderIDToPass = []
        orderID = request.GET.get('id')
        orderIDToPass.append(orderID)
        Update_OrderStatus(orderIDToPass)
    return render(request, 'ordersRequests.html')


def acceptAllOrders(request):
    if request.method == 'POST':
        UpdateAll_OrderStatus()
    return render(request, 'ordersRequests.html')


def orderRequestDetails(request):
    page = 'orderRequestDetails.html'
    context = {}
    if request.method == 'GET':
        token = request.session.get('login_token')
        if token is not None:
            page = 'orderRequestDetails.html'
            orderID = request.GET.get('orderID')
            orders = list(getOrder(orderID))
            orderList = []
            for element in orders:
                for character in element:
                    print("character", character)
                    data = character.split(',')
                    orderID = data[0].strip("()")
                    customerID = data[1]
                    date = data[2]
                    orderTotal = data[3]
                    status = data[4]
                    productID = data[5]
                    productPrice = data[6].strip(")")
                    customer = getUserByID(customerID)
                    customerName = customer['name']
                    product = getProductMongoDB(productID)
                    vendorRole = product['roleVendor']
                    if vendorRole == "XPTO":
                        vendorName = vendorRole
                    elif vendorRole == "parceiro":
                        vendorID = product['vendor']
                        vendorProfile = getUserByID(vendorID)
                        vendorName = vendorProfile['name']
                    productName = product['productName']

                    orderList.append(
                        {'productName': productName, 'productPrice': productPrice, 'vendorName': vendorName})

            context = {'orderList': orderList, 'customerName': customerName, 'orderTotal': orderTotal,
                       'orderID': orderID, 'date': date, 'status': status, }
    return render(request, page, context=context)
