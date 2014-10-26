from api.models import Tick
from django_cron import CronJobBase, Schedule
from decimal import Decimal
from crons import ALL_Markets, HEADER
import urllib2
import json


class TickerCron(CronJobBase):
    # every 5 minutes
    RUN_EVERY_MINS = 1
    RETRY_AFTER_FAILURE_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    #getcontext().prec = 13
    
    code = 'crons.ticker_cron'    # a unique code

    def do(self):
        print "Starting Ticker Cron"
        # 30 requests
        for from_currency, market in ALL_Markets.iteritems():
            for to_currency in market:
                url = 'https://cex.io/api/ticker/%s/%s' % (to_currency, from_currency)
                req = urllib2.Request(url, headers=HEADER)
                serialized_data = urllib2.urlopen(req).read()
                data = json.loads(serialized_data)
                if data.get('error'):
                    print "ERROR: ", data.get('error')
                    continue
                tick = Tick()
                tick.bid = data['bid']
                tick.ask = data['ask']
                tick.currency1 = from_currency
                tick.currency2 = to_currency
                tick.low = Decimal(data['low'])
                tick.high = Decimal(data['high'])
                tick.volume = Decimal(data['volume'])
                tick.last = Decimal(data['last'])
                tick.save()
        print "Ending Ticker Cron %s requests" % 30
