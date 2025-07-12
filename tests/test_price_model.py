from datetime import datetime
from src.price_model import PriceModel

def test_price_model_with_realistic_csv():
    csv_data = """ts_start,ts_end,price
2025-07-13 00:00:00,2025-07-13 01:00:00,0.004440
2025-07-12 23:00:00,2025-07-13 00:00:00,0.006310
2025-07-12 22:00:00,2025-07-12 23:00:00,0.012290
"""
    price_model = PriceModel(price_data_csv = csv_data)
    query_time = datetime(2025, 7, 12, 23, 45)

    expected_price = 0.006310
    actual_price = price_model.get_price(query_time)
    assert actual_price == expected_price

