# TickVault Python Query API

Python API that provides programmatic access to micro and nanosecond-scale trading data on a TickVault platform from TickSmith. Portals with accessible data include [Thomson Reuters Tick History](https://trdata.tickvault.com) and [Nasdaq-CX](https://nasdaq-cx.ticksmith.com).

## Installation

Using pip:
```bash
pip install tickvault-python-api
```

## Example Usage

Get the bid/ask spread of TD on CHIX on May 4th, 2017 
```python
from tickvaultpythonapi.nasdaqcxclient import NasdaqCxClient
 
nasdaq = NasdaqCxClient(user_name=<USER_NAME>, secret_key=<API_KEY>)

result = nasdaq.query_hits(source="CHIX", tickers="td",
                           fields="ts,askprice,bidprice",
                           start_time=20170504093000, end_time=20170504160000,
                           predicates="ask_size > 10 and bid_size > 10 and line_type like Q",
                           limit=1000000)

df = nasdaq.as_dataframe(result)

df.plot()
```