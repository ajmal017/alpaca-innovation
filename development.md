### Notes and Thoughts...

Don't mess with the base installation of python and stuff. Do dangerous stuff in a virtualenv... speaking of that, figure out which python venv you want to use and stick to.

After poking around the source code for `alpaca_trade_api` it's a lot more obvious what is going on with the StreamConn instance. So it does connect with polygon with the regex. Decorator comprehension is a bit shaky but I'll get to that sometime later this year.

Proof of concept for database connection and loading is done. Now what is needed is to check accuracy and any drops.

Second implementation goal is postgresql, if directly inside heroku.

Concurrently, heroku deployment requires wrapping inside a Flask app.


In reality the actual use of second-by-second data isn't that useful. Streaming is useful for live trading in that it protects closer to the triggered stop losses (but those should be set at the beginning of each strategy execution - unless these boundaries change due to circumstances, which arguably won't be a point reached anytime soon)

In any case, right now it is appropiate to look at second-by-second data only to analyze exactly how fast circumstances the market changes at critical junctures.

For example, something hapapened on 8/16/2019 which caused a massive vol and price spike at 7:21AM PST. But that spike died down immediately.

So when you have a moving average of the vol with _second by second data_ it becomes much eaiser to have that system in place.

After all, it is largely a random walk, as I subscribe to weak form efficiency.

What these are useful for are signals (at this point, mostly just signals if something dramatic happens in seconds)...

Start reading on Waves and Other Vibrations.

Ideally your strategy will take "snapshots" aand say, given this and the current "priced-in-ness", what is the "edge/insight" that causes this pattern to sustain/be broken?

### Development Goal:

Right now the plan is to have a data streaming solution from the Alpaca/Polygon endpoint to your own database for real time analytics.

Alpaca/Polygon.io --websocket--> Flask app (wrapped inside Heroku) --> "Data Lake" (mysql/postgres prod, sqlite dev?) --> Analytics pull from the database and are triggered by Flask. 

Considerations:

1. There is probably a smarter way to establish a connection for direct callbacks between Flask and science. Perhaps that can be established with implementing a websocket server inside Flask?

2. Docker seems more complicated than I thought. Dockerizing the deployment will reduce a lot of pain between managing environments but will raise huge devops overhead.

3. Should there be a FE interface linked to the websocket? if 1 is done then we can have that simply stream from one source.

4. An actual database costs money. Perhaps I can just hack that into another interface for web streaming to my own local services (or on heroku) with a centralized solution.


```python
# Sample result type Agg

data = tradeapi.polygon.entity.Agg({'average': 288.6434, 
   ...:     'close': 288.6401, 
   ...:     'dailyopen': 286.48, 
   ...:     'end': 1565983578000, 
   ...:     'high': 288.65, 
   ...:     'low': 288.64, 
   ...:     'open': 288.65, 
   ...:     'start': 1565983577000, 
   ...:     'symbol': 'SPY', 
   ...:     'totalvolume': 51252531, 
   ...:     'volume': 1814, 
   ...:     'vwap': 287.9529})

import inspect
inspect.getmembers(data)
```

data._raw is a type dict

Why the heck do they instantiate as this kind of Object?
https://github.com/alpacahq/alpaca-trade-api-python/blob/master/alpaca_trade_api/polygon/entity.py

I believe `websocket.run_forever()` directly inherits from asyncio or threading? Check it out later...
https://github.com/websocket-client/websocket-client

- it gets it from threading. Probably best to stick with asyncio for now.