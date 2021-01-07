# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 11:34:53 2020

@author: LENOVO
"""

import os
from flask import Flask, jsonify
from flaskext.mysql import MySQL
from flask import Flask, jsonify, request 

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'b43ceb664738e7'
app.config['MYSQL_DATABASE_PASSWORD'] = 'b5b7ebdc'
app.config['MYSQL_DATABASE_DB'] = 'heroku_5ef5065bba5a68a'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-02.cleardb.com'

mysql.init_app(app)

@app.route('/')
def hello():
    return "Hello world"

@app.route('/addProduct',methods=['POST'])
def add_producttocart():
    try:
        
        _json=request.json
        _Username=_json['Username']
        _Productname = _json['Productname']
        _Quantity= _json['Quantity']
        _price = _json['price']
        _purchased=_json['purchased']
  
        
        if(_Username and _Productname and _Quantity and _price and _purchased  and request.method=='POST'):
            sqlQuery="INSERT INTO pythonlogin.AddtoCart_table(Username, Productname,Quantity,price,purchased) VALUES(%s,%s,%s,%s,%s)"
            bindData= (_Username,_Productname,_Quantity,_price,_purchased)
            conn=mysql.connect()
            cursor= conn.cursor()
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            response = jsonify("Product added to cart successfully by user")
            response.status_code = 200
            return response
        else:
            return "Not post request"
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    

  
     


@app.route('/Product')
def getproducts():
    cur = mysql.connect().cursor()
    cur.execute('''select * from pythonlogin.AddtoCart_table''')
    r = [dict((cur.description[i][0], value)
                for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'myCollection' : r})

@app.route('/Product/<int:id>')
def getproduct(id):
    cur = mysql.connect().cursor()
    cur.execute("select * from pythonlogin.barcode_product where barcode=%s",id)
    r = [dict((cur.description[i][0], value)
                for i, value in enumerate(row)) for row in cur.fetchall()]
    #print(r["email"])
    return jsonify({'myCollection' : r})

@app.route('/getCartItems')
def getCartitems():
    cur = mysql.connect().cursor()
    cur.execute('''select * from pythonlogin.addtocart_table where purchased=1''')
    r = [dict((cur.description[i][0], value)
                for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'myCollection' : r})  

@app.route('/getRatingItems')
def getRatingitems():
    cur = mysql.connect().cursor()
    cur.execute('''select * from pythonlogin.Invoice_table ''')
    r = [dict((cur.description[i][0], value)
                for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'myCollection' : r})  



@app.route('/updateQty',methods=['PUT'])
def update_Qty():
    try:
        
        _json=request.json
        _row_id = _json['row_id']
        _Quantity=_json['Quantity']
      
        if(_row_id and _Quantity and request.method=='PUT'):
            sqlQuery="UPDATE pythonlogin.addtocart_table SET Quantity=%s WHERE row_id=%s"
            bindData= (_Quantity , _row_id)
            conn=mysql.connect()
            cursor= conn.cursor()
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            response = jsonify("Cart quantity updated successfully")
            response.status_code = 200
            return response
        else:
            return "Not post request"
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/updatePurchased',methods=['PUT'])
def update_Purchased():
    try:
        
        _json=request.json
        _row_id = _json['row_id']
        _purchased=_json['purchased']
      
        if(_row_id and _purchased and request.method=='PUT'):
            sqlQuery="UPDATE pythonlogin.addtocart_table SET purchased=%s WHERE row_id=%s"
            bindData= (_purchased , _row_id)
            conn=mysql.connect()
            cursor= conn.cursor()
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            response = jsonify("Cart Item discarded successfully")
            response.status_code = 200
            return response
        else:
            return "Not post request"
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()



@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_emp(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM pythonlogin.accounts WHERE id =%s", (id,))
		conn.commit()
		respone = jsonify('Employee deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()



if __name__ == '__main__':
    app.run()