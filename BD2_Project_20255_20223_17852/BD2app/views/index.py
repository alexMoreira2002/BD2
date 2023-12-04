from django.shortcuts import render

from ..database.orders import *
from ..database.products import *
from ..database.sales import *
from ..database.users import *


def index(request):
    if request.method == "GET":
        productType = list(getAllProductTypeMongoDB())
        productTypeList = []
        userId = request.session.get('user_id')
        if userId is not None:
            topProducts = []
            userRole = int(getUserRole(userId))
            print("UserID:", userId)
            print("UserRole:", userRole)

            if userRole == 0:
                topProduct = getMostPopularProduct()
                topProductWeek = getMostPopularProductThisWeek()
                bestSale = getBiggestSale()
                topProductStriped = topProduct[0].strip("()")
                topProductWeekStriped = topProductWeek[0].strip("()")
                topProductImage = getProductImageMongoDB(topProductStriped)
                topProductWeekImage = getProductImageMongoDB(
                    topProductWeekStriped)
                bestSaleID = bestSale['productTypeID']
                bestSaleImage = getProductTypeImageMongoDB(
                    bestSaleID)
                print("Most popular product:", topProductStriped)
                print("Most popular product Week:", topProductWeekStriped)
                print("Best Sale:", bestSaleImage)
                for product in productType:
                    id = product['_id']
                    sale = getSaleByProductType(id)
                    productTypeList.append(
                        {'productTypeName': product['productTypeName'], 'productTypeImage': product['productTypeImage'], 'id': product['_id'], 'sale':sale})
                context = {'productTypeList': productTypeList,
                           "user": userRole, 'topProductImage': topProductImage, 'topProductWeekImage': topProductWeekImage, 'bestSaleImage': bestSaleImage,
                           'topProductStriped': topProductStriped, 'topProductWeekStriped': topProductWeekStriped, 'bestSaleID': bestSaleID}

            elif userRole == 1:
                clientes = 0
                comType1 = "2"
                comType2 = "3"
                parceiro = "4"
                admin = "1"

                clientList = []
                clientList = list(getUsersByRole(clientes))
                print("cliente", clientList)
                comType1List = []
                comType1List = list(getUsersByRole(comType1))
                print("1", comType1List)
                comType2List = []
                comType2List = list(getUsersByRole(comType2))
                print("2", comType2List)

                parceiroList = []
                parceiroList = list(getUsersByRole(parceiro))

                adminList = []
                adminList = list(getUsersByRole(admin))

                context = {'clientList': clientList, 'comType1List': comType1List,
                           'comType2List': comType2List, 'parceiroList': parceiroList,
                           'adminList': adminList, "user": userRole}

            elif userRole == 2 or userRole == 3:
                topListUsers = []
                topListPartners = []
                listReturnedTop5MostSold = []
                listReturnedTop5MostSold.append(
                    list(getTop5MostSoldProducts()))
                listReturnedTop5UsersMoreOrders = []
                listReturnedTop5UsersMoreOrders.append(
                    list(getUsersWithMoreOrdersAndHowMany()))
                listReturnedTop5Partners = []
                productsOfPartners = list(getProductsByPartner())
                listReturnedTop5Partners.append(
                    list(getMostSoldProductByPartner(productsOfPartners)))
                print("Lista dos partners", listReturnedTop5Partners[0])

                for products in listReturnedTop5MostSold:
                    i = 1
                    for product in products:
                        topProductStriped = product[0].strip("()")
                        i += 1
                        topProducts.append(
                            getProductMongoDB(topProductStriped))

                for products in listReturnedTop5UsersMoreOrders:
                    for product in products:
                        data = product
                        count = data[0]
                        userID = data[1]
                        productID = data[2]
                        user = getUserByID(userID)
                        productGiven = getProductMongoDB(productID)
                        topListUsers.append(
                            {'count': count, 'user': user, 'product': productGiven})

                for products in listReturnedTop5Partners:
                    for product in products:
                        topProductStriped = product[0].strip("()")
                        data = topProductStriped.split(",")
                        count = data[0]
                        productID = data[1]
                        print("Count:", count, "ProductID:", productID)
                        productGiven = getProductMongoDB(productID)
                        topListPartners.append(
                            {'product': productGiven, 'count': count})

                waitingForApprovalCount = countProductsWaitingForApproval()

                ordersRequestsFromPostgres = getCountOrderStatusFalse()

                for charater in ordersRequestsFromPostgres:
                    ordersRequests = charater

                context = {'topProducts': topProducts, 'topListPartners': topListPartners,'ordersRequests':ordersRequests,
                           'topListUsers': topListUsers, "user": userRole, "waitingForApprovalCount":waitingForApprovalCount}

            elif userRole == 4:
                user = getUserByID(userId)
                productList = []
                product = list(getProductByOnePartner(user['_id']))
                orders = getOrdersByOnePartner(product)

                for products in orders:
                    data = products[0].strip("()")
                    orderStripped = data.split(",")
                    productID = orderStripped[0]
                    total = orderStripped[1]
                    print("ProductID:", productID, "Total:", total)
                    product = getProductMongoDB(productID)
                    productList.append({'product': product, 'total': total})

                context = {'productList': productList, "user": userRole}

        else:
            topProduct = getMostPopularProduct()
            topProductWeek = getMostPopularProductThisWeek()
            bestSale = getBiggestSale()
            topProductStriped = topProduct[0].strip("()")
            topProductWeekStriped = topProductWeek[0].strip("()")
            topProductImage = getProductImageMongoDB(topProductStriped)
            topProductWeekImage = getProductImageMongoDB(topProductWeekStriped)
            bestSaleID = bestSale['productTypeID']
            bestSaleImage = getProductTypeImageMongoDB(
                bestSaleID)
            print("Most popular product:", topProductStriped)
            print("Most popular product Week:", topProductWeekStriped)
            print("Best Sale:", bestSale["productTypeID"])
            for product in productType:
                id = product['_id']
                sale = getSaleByProductType(id)
                productTypeList.append(
                    {'productTypeName': product['productTypeName'], 'productTypeImage': product['productTypeImage'], 'id': product['_id'], 'sale': sale})
            context = {'productTypeList': productTypeList, 'topProductStriped': topProductStriped, 'topProductWeekStriped': topProductWeekStriped,
                       'bestSaleID': bestSaleID, "user": 0, 'topProductImage': topProductImage, 'topProductWeekImage': topProductWeekImage, 'bestSaleImage': bestSaleImage}
        return render(request, 'index.html', context=context)
