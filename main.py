from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient
from yahoo_fin import stock_info as si
import argparse
import math
import os
import schedule
import time

parser = argparse.ArgumentParser(
    prog = 'ticker',
    description = 'Uses YahooFinance to pull ticker data and post to InfluxDB'
)
parser.add_argument(
    '-a',
    '--auth_token',
    type=str,
    default=os.environ['AUTH_TOKEN']
)
parser.add_argument(
    '-b',
    '--bucket',
    type=str,
    default=os.environ['BUCKET']
)
parser.add_argument(
    '-o',
    '--org-name',
    type=str,
    default=os.environ['ORG_NAME']
)
parser.add_argument(
    '-p',
    '--period',
    type=int,
    default=os.environ['PERIOD']
)
args = parser.parse_args()

def ticker_symbols():
    si100 = si.tickers_ftse100()
    si250 = si.tickers_ftse250()
    ftse = si100 + si250

    return ftse


def ticker_data(tickers):
    records = []
    failed_tickers = []

    for ticker in sorted(tickers):
        live_price = ''

        try:
            live_price = si.get_live_price(ticker)

        except:
            failed_tickers.append(ticker)

        if live_price != '' and not math.isnan(live_price):
            records.append({
                "measurement": "ticker",
                "tags": {"symbol": ticker},
                "fields": {"p": live_price},
                "datetime": time.time()
            })

    return records, failed_tickers


def send_data(influx, data):
    client = InfluxDBClient(url="http://influxdb:8086", token=influx.auth_token, org=influx.org_name)
    write_api = client.write_api(write_options=SYNCHRONOUS)
                
    for record in data:
        write_api.write(bucket=influx.bucket, record=record)
        client.close()

    return


def func():
    print(time.time(), " Fetching available tickers")
    ftse = ticker_symbols()
    print(time.time(), " Fetching ticker data")
    record_data, failed = ticker_data(ftse)
    print(time.time(), " Writing ticker data to influxdb")
    send_data(args, record_data)

    if failed:
        print(time.time(), "Failed to fetch data for the following tickers:\n", failed)


schedule.every(args.period).minutes.do(func)

while True:
    schedule.run_pending()
    time.sleep(1)
