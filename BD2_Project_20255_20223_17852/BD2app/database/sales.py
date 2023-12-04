import uuid
import pymongo
from BD2app.database import MongoConn

# Connect to the MongoDB database
mongo_client = pymongo.MongoClient(MongoConn.ConnString)['BD2Project']


def createSale(productTypeID, sale):
    doc_id = str(uuid.uuid4())
    sale = {
        '_id': doc_id,
        'productTypeID': productTypeID,
        'sale': sale
    }
    if mongo_client['Sales'].insert_one(sale):
        return True
    else:
        return False


def getSales():
    sales = mongo_client['Sales'].find()
    return sales


def deleteSaleByProductType(productTypeID):
    if mongo_client['Sales'].delete_one({'productTypeID': productTypeID}):
        return True
    else:
        return False


def deleteSaleByID(saleID):
    if mongo_client['Sales'].delete_one({'_id': saleID}):
        return True
    else:
        return False


def getProductTypeBySale(saleID):
    sale = mongo_client['Sales'].find_one({'_id': saleID})
    return sale['productTypeID']


def getSaleByProductType(productTypeID):
    sale = mongo_client['Sales'].find_one({'productTypeID': productTypeID})
    if sale is not None:
        return sale
    else:
        return None


def getBiggestSale():
    sales = mongo_client['Sales'].find().sort('sale', pymongo.DESCENDING).limit(1)
    return sales.next()
