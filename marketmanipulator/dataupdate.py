__author__ = 'Zivia'

import sys

import marketmanipulator.items as it
import marketmanipulator.tradingpost as tp
import marketmanipulator.datadb as db
import marketmanipulator.datautils as du


def update_all():

    update_items()
    update_commerce_listings()
    update_commerce_prices()


def update_items(items_ids=None):

    if items_ids is None:

        db.drop_table('scratch_items')
        db.create_table(items_table_name='scratch_items')

        items_ids = it.items()

        items_ids_len = len(items_ids)
        items_ids_counter = 0

        items_ids_groups = du.chunks(items_ids, 200)

        for items_ids_group in items_ids_groups:

            items = it.items(items_ids_group)

            items_ids_counter += len(items_ids_group)
            sys.stdout.write("\rUpdating Items: %d%%" % int(100 * float(items_ids_counter) / items_ids_len))
            sys.stdout.flush()

            db.insert(items=items, scratch=True)

    else:

        items = it.items(items_ids)

        db.remove(items_ids=items_ids, scratch=True)
        db.insert(items=items, scratch=True)

    print


def update_commerce_listings(commerce_listings_ids=None):

    if commerce_listings_ids is None:

        db.drop_table('scratch_commerce_listings_buy')
        db.drop_table('scratch_commerce_listings_sell')
        db.create_table(commerce_listings_table_name='scratch_commerce_listings')

        commerce_listings_ids = tp.commerce_listings()

        commerce_listings_ids_len = len(commerce_listings_ids)
        commerce_listings_ids_counter = 0

        commerce_listings_ids_groups = du.chunks(commerce_listings_ids, 200)

        for commerce_listings_ids_group in commerce_listings_ids_groups:

            commerce_listings = tp.commerce_listings(commerce_listings_ids_group)

            commerce_listings_ids_counter += len(commerce_listings_ids_group)
            sys.stdout.write("\rUpdating Commerce Listings: %d%%" % int(100 * float(commerce_listings_ids_counter) / commerce_listings_ids_len))
            sys.stdout.flush()

            db.insert(commerce_listings=commerce_listings, scratch=True)

    else:

        commerce_listings = tp.commerce_listings(commerce_listings_ids)

        db.remove(commerce_listings_ids=commerce_listings_ids, scratch=True)
        db.insert(commerce_listings=commerce_listings, scratch=True)

    print


def update_commerce_prices(commerce_prices_ids=None):

    if commerce_prices_ids is None:

        db.drop_table('scratch_commerce_prices')
        db.create_table(commerce_prices_table_name='scratch_commerce_prices')

        commerce_prices_ids = tp.commerce_prices()

        commerce_prices_ids_groups = du.chunks(commerce_prices_ids, 200)

        commerce_prices_ids_len = len(commerce_prices_ids)
        commerce_prices_ids_counter = 0

        for commerce_prices_ids_group in commerce_prices_ids_groups:

            commerce_prices = tp.commerce_prices(commerce_prices_ids_group)

            commerce_prices_ids_counter += len(commerce_prices_ids_group)
            sys.stdout.write("\rUpdating Commerce Prices: %d%%" % int(100 * float(commerce_prices_ids_counter) / commerce_prices_ids_len))
            sys.stdout.flush()

            db.insert(commerce_prices=commerce_prices, scratch=True)

    else:

        commerce_prices = tp.commerce_prices(commerce_prices_ids)

        db.remove(commerce_prices_ids=commerce_prices_ids, scratch=True)
        db.insert(commerce_prices=commerce_prices, scratch=True)

    print


if __name__ == "__main__":

    update_items()
    update_commerce_listings()
    update_commerce_prices()
