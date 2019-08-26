#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 20:56:37 2019
"""

import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import pytz
import asyncio
import os
import dataset

# The assumption is that websocket messages are TCP will not be lost even on async/await.

key = os.environ['ALPACA_KEY_PAPER'] # These are paper endpoints
secret = os.environ['ALPACA_SECRET_PAPER']
endpoint = 'https://paper-api.alpaca.markets'

db = dataset.connect('sqlite:///SPY_QQQ_VXX_paper.db')

api = tradeapi.REST(key, secret, endpoint, 'v1')
conn = tradeapi.stream2.StreamConn(key, secret, endpoint)


async def _insert_db(bar):
    data = bar._raw
    table = db[data['symbol']]
    table.insert(data)
    return

# has to be defined before being called

@conn.on(r'^account_updates$')
async def on_account_updates(conn, channel, account):
    print('account', account)

@conn.on(r'^status$')
async def on_status(conn, channel, data):
    print('polygon status update', data)

@conn.on(r'^AM$', symbols=['SPY'])
async def on_minute_bars(conn, channel, bar):
    print('bars', bar)

@conn.on(r'^A$', symbols=['SPY', 'QQQ', 'VXX'])
async def on_second_bars(conn, channel, bar):
    print('bars', bar)
    await _insert_db(bar)


symbol = "SPY" # Still not sure how exactly this works. Look into the polygon docs later.
# https://github.com/alpacahq/alpaca-trade-api-python/tree/master/alpaca_trade_api/polygon

@conn.on(r'Q\.' + symbol)
async def on_quote(conn, channel, data):
    # Quote update received
    print(data)
    
asyncio.run(conn.run(['A.SPY', 'A.QQQ', 'A.VXX']))

# There's no need to interact with the Polygon layer at all? Just treat it as a black box...

# Best practices for data streaming? Data warehousing should technically go into something like Snowflake.
