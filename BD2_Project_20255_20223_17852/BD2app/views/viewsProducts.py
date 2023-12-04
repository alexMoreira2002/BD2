import base64
import io
import json
import os

from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404
from lxml import etree

from ..database.orders import *
from ..database.products import *
from ..database.sales import *
from ..database.users import *


def listProducts(request):
    if request.method == 'GET':
        productType_id = request.GET.get('id')
        products = list(getAllActiveProductsByType(productType_id))
        productType = getOneProductTypeMongoDB(productType_id)

        mostSoldProductID = getMostSoldProductByType(productType_id)
        if mostSoldProductID is not None:
            mostSoldProductIDStripped = mostSoldProductID[0].strip("()")
            print(mostSoldProductIDStripped)
        else:
            # default image if no product is sold
            mostSoldProductIDStripped = '6c47f393-7731-4119-81b4-6bfe1891be5e'
        mostSoldProductFinal = getProductMongoDB(mostSoldProductIDStripped)

        productList = []
        sale = getSaleByProductType(productType_id)
        for product in products:
            productList.append(
                {'productName': product['productName'], 'productImage': product['productImage'], 'productPriceStart': product['productPriceStart'], 'productPriceEnd': product['productPriceEnd'], 'id': product['_id'], 'productDescription': product['productDescription']})
        context = {'productType': productType, 'productList': productList,
                   'mostSoldProduct': mostSoldProductFinal['productImage'],'sale':sale}
    return render(request, 'listProducts.html', context=context)


def product(request):
    if request.method == 'GET':
        product_id = request.GET.get('id')
        product = getProductMongoDB(product_id)
        vendorRole = product['roleVendor']

        if vendorRole == "XPTO":
            vendor = vendorRole
        elif vendorRole == "parceiro":
            vendorID = product['vendor']
            vendorProfile = getUserByID(vendorID)
            vendor = vendorProfile['name']
    return render(request, 'product.html', {'product': product, 'id': product_id, 'vendor': vendor})


def addProduct(request):
    userId = request.session.get('user_id')
    context = {}
    if request.method == 'POST':
        imageToConvert = io.BytesIO(request.FILES['productImage'].read())
        image_data = imageToConvert.read()
        image_name = request.FILES['productImage'].name

        base64_image_data = base64.encodebytes(image_data)

        role = getUserRole(userId)
        roleVendor = ""
        productStatus = None
        if role == "1" or role == "2" or role == "3":
            roleVendor = "XPTO"
            productStatus = 1 #Fica logo ativo
        elif role == "4":
            roleVendor = "parceiro"
            productStatus = 2 #Necessita de ser aceite pelo comercial
        product = {
            'productName': request.POST['productName'],
            'productImage': image_name,
            'productPriceStart': request.POST['productPriceStart'],
            'productType': request.POST['productType'],
            'productQuantity': request.POST['productQuantity'],
            'productDescription': request.POST['productDescription'],
            'productStatus': productStatus,
            'vendor': userId,
            'roleVendor': roleVendor
        }
        result = insertProductMongoDB(
            product['productName'], product['productImage'], product['productPriceStart'], product['productType'], product['productQuantity'], product['productDescription'], product['productStatus'], product['vendor'], product['roleVendor'])
        if result:
            decoded_image_data = base64.decodebytes(base64_image_data)
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, '..\\static\\img\\'+image_name)
            with open(filename, "wb") as fh:
                fh.write(decoded_image_data)
            print('Product added successfully')
            return redirect('listAllProducts')
    elif request.method == 'GET':
        productType = list(getAllProductTypeMongoDB())
        productTypeList = []
        for product in productType:
            productTypeList.append(
                {'productTypeName': product['productTypeName'], 'productTypeImage': product['productTypeImage'], 'id': product['_id']})

        context = {'productTypeList': productTypeList}
    return render(request, 'addProduct.html', context=context)


def addProductType(request):
    if request.method == 'POST':
        imageToConvert = io.BytesIO(request.FILES['productTypeImage'].read())
        image_data = imageToConvert.read()
        image_name = request.FILES['productTypeImage'].name

        base64_image_data = base64.encodebytes(image_data)

        productType = {
            'productTypeName': request.POST['productTypeName'],
            'productTypeImage': image_name,
        }
        result = insertProductTypeMongoDB(
            productType['productTypeName'], productType['productTypeImage'])
        if result:
            print(productType['productTypeImage'])
            decoded_image_data = base64.decodebytes(base64_image_data)
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, '..\\static\\img\\'+image_name)
            with open(filename, "wb") as fh:
                fh.write(decoded_image_data)
            print('Product Type added successfully')
            messages.success(
                request, 'Tipo de produto adicionado com sucesso!')
            return redirect('addProductType')
    context = {}
    return render(request, 'addProductType.html', context=context)
    

def listAllProducts(request):
    userId = request.session.get('user_id')
    userInfo = getUserByID(userId)
    role = userInfo['role']
    userName = userInfo['name']
    if request.method == 'GET':
        productTypes = list(getAllProductTypeMongoDB())
        productTypeList = []
        for productType in productTypes:
            productTypeID = productType['_id']
            products = list(getProductsByTypeMongoDB(productTypeID))
            productTypeList.append(
                {'productTypeName': productType['productTypeName']})
            productList = []
            for product in products:
                vendorRole = product['roleVendor']

                if vendorRole == "XPTO":
                    vendor = vendorRole
                elif vendorRole == "parceiro":
                    vendorID = product['vendor']
                    vendorProfile = getUserByID(vendorID)
                    vendor = vendorProfile['name']
                print("Product Status: ", product['productStatus'])
                productList.append(
                    {'productName': product['productName'], 'productPriceStart': product['productPriceStart'], 'productPriceEnd': product['productPriceEnd'], 'id': product['_id'], 'productDescription': product['productDescription'], 'quantity': product['productQuantity'], 'vendor': vendor, 'productStatus': product['productStatus']})

            productTypeList.append({'productList': productList})
    return render(request, 'listAllProducts.html', {'productTypeList': productTypeList, 'role': role, 'userName': userName})


def deleteProduct(request):
    if request.method == 'POST':
        product_id = request.GET.get('id')
        updateProductStatus(product_id)
    return render(request, 'listAllProducts.html')


def updateProduct(request):
    productUpdate_id = request.GET.get('id')
    productTypeList = []
    if request.method == 'GET':
        productUpdate = getProductMongoDB(productUpdate_id)

        productType = list(getAllProductTypeMongoDB())
        for product in productType:
            productTypeList.append(
                {'productTypeName': product['productTypeName'], 'productTypeImage': product['productTypeImage'], 'id': product['_id']})

    else:
        imageToConvert = io.BytesIO(request.FILES['productImage'].read())
        image_data = imageToConvert.read()
        image_name = request.FILES['productImage'].name

        base64_image_data = base64.encodebytes(image_data)

        productStatusCheckBox = request.POST.get('productStatus')
        if productStatusCheckBox is not None:
            productStatus = 1
        else:
            productStatus = 0
        print("PRODUCT STATUS", productStatus)
        productUpdate = {
            'productName': request.POST['productName'],
            'productImage': image_name,
            'productPriceStart': request.POST['productPriceStart'],
            'productType': request.POST['productType'],
            'productQuantity': request.POST['productQuantity'],
            'productDescription': request.POST['productDescription'],
            'productStatus': productStatus,
        }
        result = updateProductMongoDB(
            productUpdate_id, productUpdate['productName'], productUpdate['productImage'], productUpdate['productPriceStart'], productUpdate['productType'], productUpdate['productQuantity'], productUpdate['productDescription'], productUpdate['productStatus'])
        if result:
            decoded_image_data = base64.decodebytes(base64_image_data)
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, '..\\static\\img\\'+image_name)
            with open(filename, "wb") as fh:
                fh.write(decoded_image_data)
            print('Product update successfully')
            return redirect('listAllProducts')
        else:
            print('Error in product update')

    return render(request, 'updateProduct.html', {'productUpdate': productUpdate, 'id': productUpdate_id, 'productTypeList': productTypeList})


def getSoldsByPartner(request):
    if request.method == 'GET':
        userId = request.session.get('user_id')
        if userId is not None:
            orders = []
            productsOfPartners = list(getProductsByPartner())
            orders.append(
                list(getMostSoldProductByPartner(productsOfPartners)))

            ordersList = []
            for element in orders:
                for character in element:
                    data = str(character).split(',')
                    count = data[0].strip("('())")
                    productID = data[1].strip(" ')' ")

                    product = getProductMongoDB(productID)
                    ordersList.append(
                        {'count': count, 'product': product})

    return render(request, 'getSoldProductByPartner.html', {'ordersList': ordersList})


def listUnconfirmedProducts(request):
    if request.method == 'GET':
        products = list(getProductsByStatus())
        productList = []
        for product in products:
            productList.append(
                {'productName': product['productName'], 'productPriceStart': product['productPriceStart'], 'id': product['_id'], 'productDescription': product['productDescription'], 'roleVendor': product['roleVendor']})
    return render(request, 'productRequests.html', {'productList': productList})


def confirmProduct(request):
    if request.method == 'POST':
        product_id = request.GET.get('id')
        setProductStatusActive(product_id)
    return render(request, 'productRequests.html')

def rejectProduct(request):
    if request.method == 'POST':
        product_id = request.GET.get('id')
        deleteOneProduct(product_id)
    return render(request, 'productRequests.html')

def confirmAllProducts(request):
    if request.method == 'POST':
        setAllProductsActive()
    return render(request, 'productRequests.html')

def downloadProductsJsonFile(request):
    if request.method == 'GET':
        result = exportProductsToJson()
        if result is not False:
            file_path = result
            try:
                with open(file_path, 'rb') as json_file:
                    data = json.load(json_file)
                response = HttpResponse(json.dumps(data, indent=4), content_type="application/json")
                file_name = file_path.split('\\json\\')[1]
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                print('Products exported successfully')
                return response
            except FileNotFoundError:
                raise Http404("File does not exist")
        else:
            print('Error in export products')
    return render(request, 'listAllProducts.html')

def downloadProductsXMLFile(request):
    if request.method == 'GET':
        result = exportProductsToXML()
        if result is not False:
            file_path = result
            try:
                with open(file_path, 'rb') as xml_file:
                    data = etree.fromstring(xml_file.read())
                response = HttpResponse(etree.tostring(data, pretty_print=True), content_type="application/xml")
                file_name = file_path.split('\\xml\\')[1]
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                print('Products exported successfully')
                return response
            except FileNotFoundError:
                raise Http404("File does not exist")
        else:
            print('Error in export products')
    return render(request, 'listAllProducts.html')