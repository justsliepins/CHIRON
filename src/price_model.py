import csv
from datetime import datetime
from io import StringIO

class PriceModel:
    def __init__(self, price_data_csv):
        """
        Parses CSV price data into a dictionary mapping hour start timestamps to prices.
        Expects columns: ts_start, ts_end, price
        """
        self.prices = {}
        reader = csv.DictReader(StringIO(price_data_csv))
        for row in reader:
            ts_start = datetime.strptime(row["ts_start"], "%Y-%m-%d %H:%M:%S")
            price = float(row["price"])
            self.prices[ts_start] = price

    def get_price(self, timestamp):
        """
        Returns the electricity price for the hour containing the given timestamp.

        Assumes exact hourly timestamps are keys, so rounds down query timestamp to hour.
        """
        ts_hour = timestamp.replace(minute=0, second=0, microsecond=0)
        return self.prices.get(ts_hour, None)