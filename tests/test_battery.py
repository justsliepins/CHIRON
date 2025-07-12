from src.battery import Battery

def test_battery_update_soc():
    battery = Battery(capacity_kwh = 46, current_soc = 0.2)
    battery.update_soc(power_kw=23, time_seconds=3600)
    assert abs(battery.current_soc - 0.70) < 1e-6
