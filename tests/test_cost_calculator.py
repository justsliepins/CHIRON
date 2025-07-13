from datetime import datetime, timezone
from src.Models.price_model import PriceModel
import math
import numpy as np
from src.Models.degradation_model import DegradationModel  
from src.cost_calculator import CostCalculator

def test_cost_calculator_electricity_cost():
    csv_data = """ts_start,ts_end,price
2025-07-12 14:00:00,2025-07-12 15:00:00,0.25
"""
    price_model = PriceModel( price_data_csv = csv_data )
    cost_calculator = CostCalculator( price_model = price_model )

    power_kw = 40
    time_seconds = 1800  # 30 minutes
    timestamp = datetime.fromisoformat( "2025-07-12T14:15:00+00:00" )

    cost = cost_calculator.get_electricity_cost( power_kw, time_seconds, timestamp )
    assert abs(cost - 5.00) < 1e-6

def test_calendar_ageing_cost_interpolation():
    cost_calculator = CostCalculator(price_model=None)

    soc = 0.75  
    time_seconds = 7200  

    expected_rate = np.interp(soc, [0.0, 0.5, 1.0], [0.037, 0.092, 0.204])
    expected_cost = expected_rate * (time_seconds / 3600)

    cost = cost_calculator.get_calendar_ageing_cost(soc, time_seconds)
    assert math.isclose(cost, expected_cost, abs_tol=1e-3)

 