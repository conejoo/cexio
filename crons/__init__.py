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

#HEADER

HEADER = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive'
}