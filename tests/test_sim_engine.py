from datetime import datetime
from src.battery import Battery
from src.degradation_model import DegradationModel
from src.cost_calculator import CostCalculator
from src.price_model import PriceModel
from src.simulation_engine import SimulationEngine

def test_sim_stem():
    battery = Battery(capacity_kwh = 46.0, initial_soc = 0.5)
    degradation_model = DegradationModel()
    price_model = PriceModel("ts_start,ts_end,price\n2025-07-13 10:00:00,2025-07-13 11:00:00,0.25\n")
    cost_calculator = CostCalculator(price_model, degradation_model)
    engine = SimulationEngine(battery, cost_calculator)

    power_kw = 23.0
    time_seconds = 1800
    timestamp = datetime.fromisoformat("2025-07-13T10:15:00+00:00")    
    cycle_number = 1

    result = engine.run_step(power_kw, time_seconds, timestamp, cycle_number)

    expected_soc = 0.5 + ((23.0 * 0.5) / 46.0)  # 0.75
    assert abs(result['new_soc'] - expected_soc) < 1e-6
    assert result['total_cost'] > 0
    assert result['electricity_cost'] > 0
    assert result['calendar_ageing_cost'] > 0
    assert result['cyclic_ageing_cost'] > 0

