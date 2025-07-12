import math
from src.degradation_model import DegradationModel

def test_sei_cost_decreases_with_cycle_number():
    degradation_model = DegradationModel()

    cost_cycle_1 = degradation_model.get_sei_cost(1)
    cost_cycle_200 = degradation_model.get_sei_cost(200)

    assert cost_cycle_1 > cost_cycle_200
    assert math.isclose(cost_cycle_1, 0.01, abs_tol=1e-5)
    assert math.isclose(cost_cycle_200, 0.001, abs_tol=1e-5)
