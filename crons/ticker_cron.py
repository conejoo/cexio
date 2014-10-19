from api.models import Tick
from django_cron import CronJobBase, Schedule
from decimal import Decimal
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
        USD_Market = ['BTC', 'GHS', 'LTC', 'DOGE', 'DRK']
        BTC_Market = ['GHS', 'LTC', 'DOGE', 'DRK', 'NMC', 'IXC', 'POT', 'ANC', 'MEC', 'WDC', 'FTC', 'DGB', 'USDE', 'MYR', 'AUR']
        LTC_Market = ['GHS', 'DOGE', 'DRK', 'MEC', 'WDC', 'ANC', 'FTC']
        EUR_Market = ['BTC', 'LTC', 'DOGE']

        # 30 Requests

        ALL_Markets = {
            'USD': USD_Market,
            'BTC': BTC_Market,
            'LTC': LTC_Market,
            'EUR': EUR_Market
        }

        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive'
        }
        for from_currency, market in ALL_Markets.iteritems():
            print from_currency
            for to_currency in market:
                print to_currency
                url = 'https://cex.io/api/ticker/%s/%s' % (to_currency, from_currency)
                req = urllib2.Request(url, headers=hdr)
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
                break
