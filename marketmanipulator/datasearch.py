__author__ = 'Zivia'

import items as it
import tradingpost as tp
import datautils as du
from texttable import Texttable


def search_commerce_listings(ids=None):

    buy_results = list()
    buy_results.append(['Buy Listings', 'Buy Unit Price', 'Buy Quantity'])
    sell_results = list()
    sell_results.append(['Sell Listings', 'Sell Unit Price', 'Sell Quantity'])

    # Fetch commerce listings data.
    commerce_listings = tp.commerce_listings(ids)

    for commerce_listing in commerce_listings:

        print 'Commerce Listing Data for ' + it.items(commerce_listing[u'id'])[0][u'name'] + '\n'

        for x in xrange(len(commerce_listing[u'buys'])):

            buy_listings = commerce_listing[u'buys'][x][u'listings']
            buy_unit_price = du.format_coin(commerce_listing[u'buys'][x][u'unit_price'])
            buy_quantity = commerce_listing[u'buys'][x][u'quantity']

            buy_results.append([buy_listings, buy_unit_price, buy_quantity])

        for x in xrange(len(commerce_listing[u'sells'])):

            sell_listings = commerce_listing[u'sells'][x][u'listings']
            sell_unit_price = du.format_coin(commerce_listing[u'sells'][x][u'unit_price'])
            sell_quantity = commerce_listing[u'sells'][x][u'quantity']

            sell_results.append([sell_listings, sell_unit_price, sell_quantity])

        # Tables for pretty printing.
        buy_table = Texttable()
        buy_table.set_deco(Texttable.HEADER)
        buy_table.set_cols_dtype(['t', 't', 't'])
        buy_table.set_cols_align(['r', 'r', 'r'])
        buy_table.add_rows(buy_results)

        sell_table = Texttable()
        sell_table.set_deco(Texttable.HEADER)
        sell_table.set_cols_dtype(['t', 't', 't'])
        sell_table.set_cols_align(['r', 'r', 'r'])
        sell_table.add_rows(sell_results)

        print buy_table.draw() + '\n'
        print sell_table.draw() + '\n'


def search_commerce_prices(ids=None):

    search_results = list()
    search_results.append(['Item Name', 'Buy Price', 'Sell Price', 'Demand', 'Supply'])

    for id in ids:

        # Fetch item data.
        item = it.items(id)

        item_name = item[0][u'name']

        # Fetch commerce price data.
        commerce_price = tp.commerce_prices(id)

        buy_price = du.format_coin(commerce_price[0][u'buys'][u'unit_price'])
        sell_price = du.format_coin(commerce_price[0][u'sells'][u'unit_price'])
        demand = commerce_price[0][u'buys'][u'quantity']
        supply = commerce_price[0][u'sells'][u'quantity']

        search_results.append([item_name, buy_price, sell_price, demand, supply])

    # Table for pretty printing.
    search_table = Texttable()
    search_table.set_deco(Texttable.HEADER)
    search_table.set_cols_dtype(['t', 't', 't', 't', 't'])
    search_table.set_cols_align(['l', 'r', 'r', 'r', 'r'])
    search_table.add_rows(search_results)

    print search_table.draw() + '\n'