__author__ = 'Zivia'

import psycopg2
from psycopg2.extras import Json
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys


def version():

    con = None

    try:

        con = psycopg2.connect(database='market_manipulator', user='Zivia')
        cur = con.cursor()

        cur.execute('SELECT version()')

        print cur.fetchone()

    except psycopg2.DatabaseError, e:

        print 'Database Error: %s' % e
        sys.exit(1)

    finally:

        if con:
            con.close()


def create_database(name="market_manipulator"):

    con = None

    try:

        con = psycopg2.connect("dbname='postgres' user='Zivia'")
        cur = con.cursor()

        print 'Creating database: ' + name

        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur.execute("CREATE DATABASE " + name)

    except psycopg2.DatabaseError, e:

        print 'Database Error: %s' % e
        sys.exit(1)

    finally:

        if con:
            con.close()


def create_table(items_table_name=None, commerce_listings_table_name=None, commerce_prices_table_name=None):

    con = None

    try:

        con = psycopg2.connect("dbname='market_manipulator' user='Zivia'")
        cur = con.cursor()

        if items_table_name:

            print 'Creating Items Table: ' + items_table_name

            cur.execute("CREATE TABLE " + items_table_name +
                        " (id integer, name text, icon text, type text, rarity text, level integer,"
                        "vendor_value integer, flags text[], game_types text[], restrictions text[])")

        if commerce_listings_table_name:

            print 'Creating Commerce Listings Table (buy): ' + commerce_listings_table_name + "_buy"

            cur.execute("CREATE TABLE " + commerce_listings_table_name + "_buy" +
                        " (id integer, buy_listings integer, buy_unit_price integer, buy_quantity integer)")

            print 'Creating Commerce Listings Table (sell): ' + commerce_listings_table_name + "_sell"

            cur.execute("CREATE TABLE " + commerce_listings_table_name + "_sell" +
                        " (id integer, sell_listings integer, sell_unit_price integer, sell_quantity integer)")

        if commerce_prices_table_name:

            print 'Creating Commerce Prices Table: ' + commerce_prices_table_name

            cur.execute("CREATE TABLE " + commerce_prices_table_name +
                        "(id integer, buy_quantity integer, buy_unit_price integer, sell_quantity integer,"
                        " sell_unit_price integer)")

        con.commit()

    except psycopg2.DatabaseError, e:

        if con:
            con.rollback()

        print 'Database Error: %s' % e
        sys.exit(1)

    finally:

        if con:
            con.close()


def drop_table(name="default"):

    con = None

    try:

        con = psycopg2.connect("dbname='market_manipulator' user='Zivia'")
        cur = con.cursor()

        print 'Dropping Table: ' + name

        cur.execute("DROP TABLE IF EXISTS " + name)

        con.commit()

    except psycopg2.DatabaseError, e:

        if con:
            con.rollback()

        print 'Database Error: %s' % e
        sys.exit(1)

    finally:

        if con:
            con.close()


def select(items_ids=[], commerce_listings_ids=[], commerce_prices_ids=[], scratch=False):

    if (items_ids and commerce_listings_ids and commerce_prices_ids) is None:

        return

    if items_ids is None:

        items_ids = []

    if commerce_listings_ids is None:

        commerce_listings_ids = []

    if commerce_prices_ids is None:

        commerce_prices_ids = []

    con = None

    try:

        con = psycopg2.connect("dbname='market_manipulator' user='Zivia'")
        cur = con.cursor()

        items = None
        commerce_listings = None
        commerce_prices = None

        if len(items_ids) > 0:

            if scratch:

                cur.execute("SELECT * FROM scratch_items WHERE id IN %s;", (tuple(items_ids),))

            else:

                cur.execute("SELECT * FROM items WHERE id IN %s;", (tuple(items_ids),))

            items = cur.fetchall()

        if len(commerce_listings_ids) > 0:

            if scratch:

                cur.execute("SELECT * FROM scratch_commerce_listings WHERE id IN %s;", (tuple(commerce_listings_ids),))

            else:

                cur.execute("SELECT * FROM commerce_listings WHERE id IN %s;", (tuple(commerce_listings_ids),))

            commerce_listings = cur.fetchall()

        if len(commerce_prices_ids) > 0:

            if scratch:

                cur.execute("SELECT * FROM scratch_commerce_prices WHERE id IN %s;", (tuple(commerce_prices_ids),))

            else:

                cur.execute("SELECT * FROM commerce_prices WHERE id IN %s;", (tuple(commerce_prices_ids),))

            commerce_prices = cur.fetchall()

        return items, commerce_listings, commerce_prices

    except psycopg2.DatabaseError, e:

        print 'Database Error: %s' % e
        sys.exit(1)

    finally:

        if con:
            con.close()


def insert(items=None, commerce_listings=None, commerce_prices=None, scratch=False):

    if (items and commerce_listings and commerce_prices) is None:

        return

    if items is None:

        items = []

    if commerce_listings is None:

        commerce_listings = []

    if commerce_prices is None:

        commerce_prices = []

    con = None

    try:

        con = psycopg2.connect("dbname='market_manipulator' user='Zivia'")
        cur = con.cursor()

        if scratch:

            for item in items:

                cur.execute("INSERT INTO scratch_items "
                            "(id, name, icon, type, rarity, level, vendor_value, flags, game_types, restrictions) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            [item[u'id'], item[u'name'], item[u'icon'], item[u'type'], item[u'rarity'], item[u'level'],
                             item[u'vendor_value'], item[u'flags'], item[u'game_types'], item[u'restrictions']])

            for commerce_listing in commerce_listings:

                for buy in xrange(len(commerce_listing[u'buys'])):

                    buy_listings = commerce_listing[u'buys'][buy][u'listings']
                    buy_unit_price = commerce_listing[u'buys'][buy][u'unit_price']
                    buy_quantity = commerce_listing[u'buys'][buy][u'quantity']

                    cur.execute("INSERT INTO scratch_commerce_listings_buy" +
                                "(id, buy_listings, buy_unit_price, buy_quantity) "
                                "VALUES (%s, %s, %s, %s)",
                                [commerce_listing[u'id'], buy_listings, buy_unit_price, buy_quantity])

                for sell in xrange(len(commerce_listing[u'sells'])):

                    sell_listings = commerce_listing[u'sells'][sell][u'listings']
                    sell_unit_price = commerce_listing[u'sells'][sell][u'unit_price']
                    sell_quantity = commerce_listing[u'sells'][sell][u'quantity']

                    cur.execute("INSERT INTO scratch_commerce_listings_sell" +
                                "(id, sell_listings, sell_unit_price, sell_quantity) "
                                "VALUES (%s, %s, %s, %s)",
                                [commerce_listing[u'id'], sell_listings, sell_unit_price, sell_quantity])

            for commerce_price in commerce_prices:

                cur.execute("INSERT INTO scratch_commerce_prices "
                            "(id, buy_quantity, buy_unit_price, sell_quantity, sell_unit_price) "
                            "VALUES (%s, %s, %s, %s, %s)",
                            [commerce_price[u'id'], commerce_price[u'buys'][u'quantity'],
                             commerce_price[u'buys'][u'unit_price'], commerce_price[u'sells'][u'quantity'],
                             commerce_price[u'sells'][u'unit_price']])

        else:

            for item in items:

                cur.execute("INSERT INTO items (id, data) VALUES (%s, %s)", [item[u'id'], Json(item)])

            for commerce_listing in commerce_listings:

                cur.execute("INSERT INTO commerce_listings (id, data) VALUES (%s, %s)", [commerce_listing[u'id'], Json(commerce_listing)])

            for commerce_price in commerce_prices:

                cur.execute("INSERT INTO commerce_prices (id, data) VALUES (%s, %s)", [commerce_price[u'id'], Json(commerce_price)])

        con.commit()

    except psycopg2.DatabaseError, e:

        if con:
            con.rollback()

        print 'Database Error: %s' % e
        sys.exit(1)

    finally:

        if con:
            con.close()


def remove(items_ids=None, commerce_listings_ids=None, commerce_prices_ids=None, scratch=False):

    if (items_ids and commerce_listings_ids and commerce_prices_ids) is None:

        return

    if items_ids is None:

        items_ids = []

    if commerce_listings_ids is None:

        commerce_listings_ids = []

    if commerce_prices_ids is None:

        commerce_prices_ids = []

    con = None

    try:

        con = psycopg2.connect("dbname='market_manipulator' user='Zivia'")
        cur = con.cursor()

        if scratch:

            for item_id in items_ids:

                cur.execute("DELETE FROM scratch_items WHERE id = (%s)", [item_id])

            for commerce_listing_id in commerce_listings_ids:

                cur.execute("DELETE FROM scratch_commerce_listings_buy WHERE id = (%s)", [commerce_listing_id])
                cur.execute("DELETE FROM scratch_commerce_listings_sell WHERE id = (%s)", [commerce_listing_id])

            for commerce_price_id in commerce_prices_ids:

                cur.execute("DELETE FROM scratch_commerce_prices WHERE id = (%s)", [commerce_price_id])

        else:

            for item_id in items_ids:

                cur.execute("DELETE FROM items WHERE id = (%s)", [item_id])

            for commerce_listing_id in commerce_listings_ids:

                cur.execute("DELETE FROM commerce_listings WHERE id = (%s)", [commerce_listing_id])

            for commerce_price_id in commerce_prices_ids:

                cur.execute("DELETE FROM commerce_prices WHERE id = (%s)", [commerce_price_id])

        con.commit()

    except psycopg2.DatabaseError, e:

        if con:
            con.rollback()

        print 'Database Error: %s' % e
        sys.exit(1)

    finally:

        if con:
            con.close()
