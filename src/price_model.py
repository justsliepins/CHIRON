import csv
from datetime import datetime, timezone
from io import StringIO

class PriceModel:
    def __init__(self, price_data_csv):
        """
        Parses CSV price data into a dictionary mapping hour start timestamps to prices.
        Expects columns: ts_start, ts_end, price
        """
        self.prices = []
        csv_file = StringIO(price_data_csv)
        reader = csv.DictReader(csv_file)
        for row in reader:
            ts_start = datetime.fromisoformat(row['ts_start'])
            if ts_start.tzinfo is None:
                ts_start = ts_start.replace(tzinfo=timezone.utc)

            ts_end = datetime.fromisoformat(row['ts_end'])
            if ts_end.tzinfo is None:
                ts_end = ts_end.replace(tzinfo=timezone.utc)

            price = float(row['price'])
            self.prices.append({'ts_start': ts_start, 'ts_end': ts_end, 'price': price})

    def get_price(self, timestamp):
        """
        Returns the electricity price for the hour containing the given timestamp.

        Assumes exact hourly timestamps are keys, so rounds down query timestamp to hour.
        """
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

        for entry in self.prices:
            if entry['ts_start'] <= timestamp < entry['ts_end']:
                return entry['price']
        return None