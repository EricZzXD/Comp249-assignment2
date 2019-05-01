"""
Code for handling sessions in our web application
"""

from bottle import request, response
import uuid
import json

import model
import dbschema

COOKIE_NAME = 'session'


def get_or_create_session(db):
    """Get the current sessionid either from a
    cookie in the current request or by creating a
    new session if none are present.

    If a new session is created, a cookie is set in the response.

    Returns the session key (string)
    """
    sessionid = request.get_cookie(COOKIE_NAME)

    cur = db.cursor()
    cur.execute("SELECT sessionid FROM sessions WHERE sessionid=?", (sessionid,))
    row = cur.fetchone()

    if sessionid is not None and row is not None:
        response.set_cookie('session', str(sessionid))
        return sessionid
    else:

        # create a new session ID base on uuid4
        sessionid = str(uuid.uuid4())
        cur = db.cursor()

        # since the session ID is null, insert the sessionid into sessions append empty
        cur.execute("INSERT INTO sessions VALUES (?, ?)", (sessionid, '[]'))

        # Commit
        db.commit()

        response.set_cookie(COOKIE_NAME, str(sessionid))
        return sessionid

def add_to_cart(db, itemid, quantity):
    """Add an item to the shopping cart"""
    # get the item info from the database base on the id
    product = model.product_get(db, itemid);


    # Get the item info
    item = {
        'id': itemid,
        'name': product['name'],
        'quantity': int(quantity),
        'cost': product['unit_cost'] * int(quantity),
    }

    # get the id from session table
    session_id = get_or_create_session(db)

    # get the info fro the get_cart_contents
    cart = get_cart_contents(db)

    # append the item to the cart
    cart.append(item)

    #
    cursor = db.cursor()

    cursor.execute("DELETE FROM sessions WHERE sessionid=?", (session_id,))
    cursor.execute("INSERT INTO sessions (sessionid, data) VALUES (?, ?)", (session_id, json.dumps(cart)))
    db.commit()


def get_cart_contents(db):
    """Return the contents of the shopping cart as
    a list of dictionaries:
    [{'id': <id>, 'quantity': <qty>, 'name': <name>, 'cost': <cost>}, ...]
    """

    # Get the sessionID from the db
    SID = get_or_create_session(db)

    # Get the SessionID from the session table and see if it match
    cursor = db.cursor()
    cursor.execute("SELECT * FROM sessions WHERE sessionid=?", (SID,))

    # if it match, fetchone
    cart = cursor.fetchone()

    # Load in json formatting
    if cart:
        return json.loads(cart['data'])
    else:
        return []




