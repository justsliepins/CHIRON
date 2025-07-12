import math
import numpy as np
from src.degradation_model import DegradationModel
from src.cost_calculator import CostCalculator
from src.price_model import PriceModel

def test_sei_cost_decreases_with_cycle_number():
    degradation_model = DegradationModel(initial_cost=6.088, decay_rate=0.013)

    cost_cycle_1 = degradation_model.get_sei_cost(1)
    cost_cycle_200 = degradation_model.get_sei_cost(200)

    assert cost_cycle_1 > cost_cycle_200
    assert math.isclose(cost_cycle_1, 6.088, abs_tol=1e-5)
    assert math.isclose(cost_cycle_200, 0.457, abs_tol=1.1e-3)

def test_cost_calculator_includes_sei_degradation():
    price_model = PriceModel("ts_start,ts_end,price\n2025-07-12 14:00:00,2025-07-12 15:00:00,0.25\n")
    degradation_model = DegradationModel(initial_cost=6.088, decay_rate=0.013)
    calculator = CostCalculator(price_model, degradation_model)

    sei_cost_1 = calculator.get_sei_degradation_cost(1)
    sei_cost_200 = calculator.get_sei_degradation_cost(200)

    assert sei_cost_1 > sei_cost_200

