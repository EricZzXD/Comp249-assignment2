
import random
from bottle import Bottle, template, static_file, request, redirect, HTTPError

import model
import session

app = Bottle()

# get the css file and apply to all the html
@app.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')

# this is for index.html
@app.route('/')
def index(db):
    # session
    session.get_or_create_session(db)
    # create a string
    lis = []

    # get the product_list dict and name it as productList
    productList = model.product_list(db,None)

    # use for loop an for productList and get the id, name, url and so on for each dict
    for row in productList:
        info = {
            'id': row['id'],
            'name': row['name'],
            'url': row['image_url'],
            'inventory': row['inventory'],
            'cost': row['unit_cost']
        }

        # append those data into the lis
        lis.append(info)

        # return the title and a lis that contain all the data for each product. and use the for loop in html
    return template('index', title='The WT Store', lis=lis)



# product/id
@app.route('/product/<id>', method='GET')
def product(db, id):
    # just the product data base on id
    product = model.product_get(db, id)

    # if no such product, 404 error and print 'No such Item'
    if not product:
        return HTTPError(404,'No such Item ')
    else:
        # get the data and insert to the product.html
        info = {
            'title': product['name'],
            'id': product['id'],
            'name': product['name'],
            'url': product['image_url'],
            'inventory': product['inventory'],
            'cost': product['unit_cost'],
            'description': product['description']
            }
        # return the template with the product data

    return template('product', info)


# create a Method that handle the Product Post
# if 'quantity' in request.query:
# @app.post('/product/<id>')
# def add_to_cart(db,id):
#     session.get_cart_contents(db)
#
#     #the quantity will be request and name as quantity
#     quantity = request.forms.get['quantity']
#
#     # the data use the method of session.add_to_cart with the data
#     # id from the product/<id>
#     session.add_to_cart(db, id, quantity=quantity)
#
#     # once it works, it redirect to cart
#     return redirect('/cart')



# create a cart page
@app.route('/cart')
def cart(db):
    # session get the content from the from the db
    session.get_cart_contents(db)


    return template('cart')


if __name__ == '__main__':

    from bottle.ext import sqlite
    from dbschema import DATABASE_NAME
    # install the database plugin
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))
    app.run(debug=True, port=8010)
