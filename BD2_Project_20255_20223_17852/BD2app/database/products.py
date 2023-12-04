import os
import uuid
import pymongo
import psycopg2
import json
from lxml import etree
from datetime import date
from ..database.sales import *
from BD2app.database import MongoConn

# Connect to the MongoDB database
mongo_client = pymongo.MongoClient(MongoConn.ConnString)['BD2Project']

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    "host=localhost port=5432 dbname=BD2Project user=postgres password=postgres")


def insertProductMongoDB(productName, productImage, productPriceStart, productType,
                         productQuantity, productDescription, productStatus, vendor, roleVendor):
    doc_id = str(uuid.uuid4())  # Generate a random ID
    salesInProductType = getSaleByProductType(productType)
    if salesInProductType is not None:
        sale = salesInProductType['sale']
        newSale = float(sale)/100
        productPriceEnd = float(
            float(productPriceStart) - float(productPriceStart) * newSale)
        product = {
            '_id': doc_id,
            'productName': productName,
            'productType': productType,
            'productQuantity': productQuantity,
            'productImage': productImage,
            'productPriceStart': productPriceStart,
            'productPriceEnd': productPriceEnd,
            'productDescription': productDescription,
            'productStatus': productStatus,
            'vendor': vendor,
            'roleVendor': roleVendor
        }
    else:
        product = {
            '_id': doc_id,
            'productName': productName,
            'productType': productType,
            'productQuantity': productQuantity,
            'productImage': productImage,
            'productPriceStart': productPriceStart,
            'productPriceEnd': productPriceStart,
            'productDescription': productDescription,
            'productStatus': productStatus,
            'vendor': vendor,
            'roleVendor': roleVendor
        }
    if mongo_client['Products'].insert_one(product):
        return True
    else:
        return False


def getAllProductsMongoDB():
    products = mongo_client['Products'].find()
    return products


def getProductMongoDB(_id):
    product = mongo_client['Products'].find_one({'_id': _id})
    return product


def getProductImageMongoDB(_id):
    product = mongo_client['Products'].find_one({'_id': _id})
    return product['productImage']


def getProductTypeImageMongoDB(_id):
    product = mongo_client['ProductTypes'].find_one({'_id': _id})
    return product['productTypeImage']


def updateProductApplySaleMongoDB(productID, priceEnd):
    if mongo_client['Products'].update_one({'_id': productID}, {'$set': {'productPriceEnd': priceEnd}}):
        return True
    else:
        return False


def updateProductStatus(productID):
    if mongo_client['Products'].update_one({'_id': productID}, {'$set': {'productStatus': 0}}):
        return True
    else:
        return False


def setProductStatusActive(product_id):
    if mongo_client['Products'].update_one({'_id': product_id}, {'$set': {'productStatus': 1}}):
        return True


def deleteOneProduct(product_id):
    if mongo_client['Products'].delete_one({'_id': product_id}):
        return True


def setAllProductsActive():
    if mongo_client['Products'].update_many({'productStatus': 2}, {'$set': {'productStatus': 1}}):
        return True


def getAllActiveProducts():
    products = mongo_client['Products'].find({'productStatus': 1})
    return products


def getAllActiveProductsByType(productType):
    products = mongo_client['Products'].find(
        {'productStatus': 1, 'productType': productType})
    return products


def insertProductTypeMongoDB(productTypeName, productTypeImage):
    doc_id = str(uuid.uuid4())  # Generate a random ID
    productType = {
        '_id': doc_id,
        'productTypeName': productTypeName,
        'productTypeImage': productTypeImage
    }
    if mongo_client['ProductTypes'].insert_one(productType):
        return True
    else:
        return False


def getAllProductTypeMongoDB():
    productTypes = mongo_client['ProductTypes'].find()
    return productTypes


def getOneProductTypeMongoDB(_id):
    productTypes = mongo_client['ProductTypes'].find_one({'_id': _id})
    return productTypes


def getProductsByTypeMongoDB(productType):
    products = mongo_client['Products'].find({'productType': productType})
    return products


def getProductsByPartner():
    products = mongo_client['Products'].find(
        {'roleVendor': {'$nin': ["XPTO", "Stock"]}})
    return products


def getProductByOnePartner(vendor):
    products = mongo_client['Products'].find({'vendor': vendor})
    return products


def updateProductQuantity(productID, quantity):
    if mongo_client['Products'].update_one({'_id': productID}, {'$set': {'productQuantity': quantity}}):
        return True
    else:
        return False


def countProductsWaitingForApproval():
    count = mongo_client['Products'].find({'productStatus': 2}).count()
    return count


def updateProductMongoDB(productID, productName, productImage, productPriceStart, productType, productQuantity, productDescription, productStatus):
    salesInProductType = getSaleByProductType(productType)
    if salesInProductType is not None:
        sale = salesInProductType['sale']
        newSale = float(sale)/100
        productPriceEnd = float(
            float(productPriceStart) - float(productPriceStart) * newSale)
        if mongo_client['Products'].update_one({'_id': productID},
                                               {'$set': {'productName': productName,
                                                         'productImage': productImage,
                                                         'productImage': productImage,
                                                         'productPriceStart': productPriceStart,
                                                         'productPriceEnd': productPriceEnd,
                                                         'productType': productType,
                                                         'productQuantity': productQuantity,
                                                         'productDescription': productDescription,
                                                         'productStatus': productStatus
                                                         }}):
            return True
        else:
            return False
    else:
        if mongo_client['Products'].update_one({'_id': productID},
                                               {'$set': {'productName': productName,
                                                         'productImage': productImage,
                                                         'productImage': productImage,
                                                         'productPriceStart': productPriceStart,
                                                         'productPriceEnd': productPriceStart,
                                                         'productType': productType,
                                                         'productQuantity': productQuantity,
                                                         'productDescription': productDescription,
                                                         'productStatus': productStatus
                                                         }}):
            return True
        else:
            return False


def getMostPopularProduct():  # get most popular product view
    cur = conn.cursor()
    cur.execute("SELECT * from getmostpopularproduct")
    product = cur.fetchone()
    cur.close()
    return product


def getMostPopularProductThisWeek():  # get most popular product this week view
    cur = conn.cursor()
    cur.execute("SELECT * from getmostpopularproductthisweek")
    product = cur.fetchone()
    cur.close()
    if product is not None:
        return product
    else:
        return None


def getTop5MostSoldProducts():  # get top 5 most sold products view
    cur = conn.cursor()
    cur.execute("SELECT * from gettop5mostsoldproducts")
    products = cur.fetchall()
    cur.close()
    if products is not None:
        return products
    else:
        return None


# get top 5 most sold products by user function
def getTop5MostSoldProductsByUser(userID):
    cur = conn.cursor()
    cur.execute("SELECT gettop5mostsoldproductsbyuser('%s')" % userID)
    products = cur.fetchall()
    cur.close()
    return products


# get most sold product by type function
def getMostSoldProductByType(productType):
    productName = list(getProductsByTypeMongoDB(productType))
    mostSoldProductByType = []
    for product in productName:
        mostSoldProductByType.append(product['_id'])
    cur = conn.cursor()
    cur.execute("SELECT getmostsoldproductbytype(array %s::uuid[])" %
                mostSoldProductByType)
    productID = cur.fetchone()
    cur.close()
    if productID[0] is None:
        return None
    else:
        return productID


def getUsersWithMoreOrdersAndHowMany():  # get top 5 users with more orders and how many view
    cur = conn.cursor()
    cur.execute("SELECT * from getUsersWithMoreOrdersAndHowMany")
    data = cur.fetchall()
    cur.close()
    return data


# get most sold product by partner function
def getMostSoldProductByPartner(partnerID):
    mostSoldProductByPartner = []
    for product in partnerID:
        mostSoldProductByPartner.append(product['_id'])
    cur = conn.cursor()
    cur.execute("SELECT getmostsoldproductbypartner(array %s::uuid[])" %
                mostSoldProductByPartner)
    productID = cur.fetchall()
    cur.close()
    return productID


def getSoldProductByPartner(partnerID):  # get sold product by partner function
    soldProductByPartner = []
    for product in partnerID:
        soldProductByPartner.append(product['_id'])
    cur = conn.cursor()
    cur.execute("SELECT getsoldproductbypartner(array %s::uuid[])" %
                soldProductByPartner)
    productID = cur.fetchall()
    cur.close()
    return productID


def getProductsByStatus():
    products = mongo_client['Products'].find({'productStatus': 2})
    return products


def exportProductsToJson():
    today = date.today()
    d1 = today.strftime("%d-%m-%Y")
    product = mongo_client['Products'].find()
    cur_path = os.path.dirname(__file__)
    file_path = os.path.join(cur_path, '..\\static\\json\\Products' + d1 + '.json')
    print(f"Current ---->{cur_path}")
    print(f"Final ---->{file_path}")
    try:
        with open(file_path, 'w') as f:
            json.dump(list(product), f)
        return file_path
    except:
        return False


def exportProductsToXML():
    today = date.today()
    d1 = today.strftime("%d-%m-%Y")
    product = mongo_client['Products'].find()
    cur_path = os.path.dirname(__file__)
    file_path = os.path.join(cur_path, '..\\static\\xml\\Products' + d1 + '.xml')
    print(f"Current ---->{cur_path}")
    print(f"Final ---->{file_path}")
    with open(file_path, 'w') as f:
        root = etree.Element('Products')
        for doc in product:
            product = etree.SubElement(root, 'Product')
            for key, value in doc.items():
                child = etree.SubElement(product, key)
                child.text = str(value)
        tree = etree.ElementTree(root)
        tree.write(file_path, pretty_print=True,
                   xml_declaration=True, encoding='utf-8')
    return file_path
