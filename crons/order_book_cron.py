from api.models import OrderBook
from django_cron import CronJobBase, Schedule
from decimal import Decimal
from crons import ALL_Markets, HEADER
import urllib2
import json


class OrderBookCron(CronJobBase):
    # every 5 minutes
    RUN_EVERY_MINS = 1
    RETRY_AFTER_FAILURE_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    #getcontext().prec = 13

    code = 'crons.order_book_cron'    # a unique code

    def do(self):
        print "Starting Order Book Cron"
        OrderBook.objects.all().delete()
        for from_currency, market in ALL_Markets.iteritems():
            for to_currency in market:
                url = 'https://cex.io/api/order_book/%s/%s' % (to_currency, from_currency)
                req = urllib2.Request(url, headers=HEADER)
                serialized_data = urllib2.urlopen(req).read()
                data = json.loads(serialized_data)
                if data.get('error'):
                    print "ERROR: ", data.get('error')
                    continue
                for bid_index in range(0, min(30, len(data['bids']))):
                    bid = data['bids'][bid_index]
                    order_book = OrderBook()
                    order_book.is_bid = True
                    order_book.amount = Decimal(bid[1])
                    order_book.price = bid[0]
                    order_book.currency1 = from_currency
                    order_book.currency2 = to_currency
                    order_book.save()
                for bid_index in range(0, min(30, len(data['asks']))):
                    bid = data['asks'][bid_index]
                    order_book = OrderBook()
                    order_book.is_bid = False
                    order_book.amount = Decimal(bid[1])
                    order_book.price = bid[0]
                    order_book.currency1 = from_currency
                    order_book.currency2 = to_currency
                    order_book.save()
        print "Ending Order Book Cron %s requests" % 30
