import uuid
import pymongo
from BD2app.database import MongoConn

# Connect to the MongoDB database
mongo_client = pymongo.MongoClient(MongoConn.ConnString)['BD2Project']


def getCartByUserMongoDB(userID):
    products = mongo_client['Cart'].find({'userID': userID})
    return products


def addProductToCart(userID, productID):
    doc_id = str(uuid.uuid4())  # Generate a random ID
    cart = {
        '_id': doc_id,
        'userID': userID,
        'productID': productID
    }
    if mongo_client['Cart'].insert_one(cart):
        return True
    else:
        return False


def removeProductFromCart(cartID):
    if mongo_client['Cart'].delete_one({'_id': cartID}):
        return True
    else:
        return False

def removeallProductsFromUserCart(userID):
    if mongo_client['Cart'].delete_many({'userID':userID}):
        return True
    else:
        return False

def getCartMongoDB(cartID):
    cart = mongo_client['Cart'].find_one({'_id': cartID})
    return cart
