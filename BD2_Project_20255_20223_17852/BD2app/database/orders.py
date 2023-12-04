import pymongo
import psycopg2
from BD2app.database import MongoConn

# Connect to the MongoDB database
mongo_client = pymongo.MongoClient(MongoConn.ConnString)['BD2Project']

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    "host=localhost port=5432 dbname=BD2Project user=postgres password=postgres")


def insertOrder(orderProductID, orderCustomer, orderPrice):  # insert order procedure
    cur = conn.cursor()
    cur.execute("CALL orders_insert(%s::uuid[], %s, %s::numeric[])",
                (orderProductID, orderCustomer, orderPrice))  # call the stored procedure
    conn.commit()
    cur.close()
    return True


def deleteOrder(orderID):  # delete order procedure
    cur = conn.cursor()
    cur.execute("CALL orders_delete(%s)" % orderID)
    conn.commit()
    cur.close()
    return True


def Update_OrderStatus(orderID):  # update order status procedure
    cur = conn.cursor()
    cur.execute("CALL update_orderstatus(array %s::int[])" % orderID)
    conn.commit()
    cur.close()
    return True


def UpdateAll_OrderStatus():  # update all order status procedure
    cur = conn.cursor()
    cur.execute("CALL updateall_orderstatus()")
    conn.commit()
    cur.close()
    return True


def getOrderStatusFalse():  # get order status false view
    cur = conn.cursor()
    cur.execute("SELECT * FROM getorderstatusfalse")
    orders = cur.fetchall()
    cur.close()
    return orders


def getCountOrderStatusFalse():  # get count order status false view
    cur = conn.cursor()
    cur.execute("SELECT * FROM getcountorderstatusfalse")
    orders = cur.fetchone()
    cur.close()
    return orders


def getOrdersByCustomer(customerID):  # get orders by customer function
    cur = conn.cursor()
    cur.execute("SELECT getordersbycustomer('%s')" % customerID)
    orders = cur.fetchall()
    cur.close()
    return orders


def getOrder(orderID):  # get order function
    cur = conn.cursor()
    cur.execute("SELECT getorder(%s)" % orderID)
    order = cur.fetchall()
    cur.close()
    return order


def getAllOrders():  # get all orders view
    cur = conn.cursor()
    cur.execute("SELECT * FROM OrdersView")
    orders = cur.fetchall()
    cur.close()
    return orders


def getUsersOrdersAndHowMany():  # get users orders and how many view
    cur = conn.cursor()
    cur.execute("SELECT * from getusersordersandhowmany")
    data = cur.fetchall()
    cur.close()
    return data


def getOrdersByOnePartner(partnerID):  # get orders by one partner function
    soldProductByPartner = []
    for product in partnerID:
        soldProductByPartner.append(product['_id'])
    cur = conn.cursor()
    cur.execute("SELECT getordersbyonepartner(array %s::uuid[])" %
                soldProductByPartner)
    orders = cur.fetchall()
    cur.close()
    return orders
