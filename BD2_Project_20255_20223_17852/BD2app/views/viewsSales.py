from django.shortcuts import render, redirect
from ..database.products import *
from ..database.sales import *


def createSales(request):
    context = {}
    page = "createSale.html"
    productType = request.GET.get('id')
    if request.method == 'POST':
        sale = request.POST.get('sale')
        sales = getSaleByProductType(productType)
        print(sales)
        if sales is not None:
            deleteSaleByProductType(productType)
        result = createSale(productType, sale)
        if result:
            productList = list(getProductsByTypeMongoDB(productType))
            for product in productList:
                productID = product['_id']
                priceStart = float(product['productPriceStart'])
                newSale = float(sale) / 100
                newPriceEnd = priceStart - priceStart * newSale
                updateProductApplySaleMongoDB(productID, newPriceEnd)
            return redirect('sales')
        else:
            context['error'] = "Error creating sale"
        productTypeGet = getOneProductTypeMongoDB(productType)
        productTypeName = productTypeGet['productTypeName']
        context = {'productTypeName': productTypeName}
    else:
        productTypeGet = getOneProductTypeMongoDB(productType)
        productTypeName = productTypeGet['productTypeName']
        context = {'productTypeName': productTypeName}
        page = "createSale.html"
    return render(request, page, context=context)


def displayProductTypes(request):
    productTypes = list(getAllProductTypeMongoDB())
    productTypesList = []
    for type in productTypes:
        productTypesList.append(
            {'productTypeName': type['productTypeName'], 'id': type['_id']})
    return render(request, 'selectTypeForSale.html', {'productTypesList': productTypesList})


def sales(request):
    sales = getSales()
    salesList = []
    for sale in sales:
        productTypeID = sale['productTypeID']
        productType = getOneProductTypeMongoDB(productTypeID)
        productTypeName = productType['productTypeName']
        salesList.append(
            {'sale': sale['sale'], 'id': sale['_id'], 'productTypeName': productTypeName})

    return render(request, 'salesOverview.html', {'salesList': salesList})


def deleteSale(request):
    saleID = request.GET.get('id')
    productTypeID = getProductTypeBySale(saleID)
    productList = list(getProductsByTypeMongoDB(productTypeID))
    result = deleteSaleByID(saleID)
    if result:
        for product in productList:
            productID = product['_id']
            priceStart = float(product['productPriceStart'])
            updateProductApplySaleMongoDB(productID, priceStart)
        return redirect('sales')
    return render(request, 'salesOverview.html')
