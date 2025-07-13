from datetime import datetime

class SimulationEngine:
    def __init__(self,  battery, cost_calculator):
        """
        Args:
            battery (Battery): Battery model with update_soc() method.
            cost_calculator (CostCalculator): Calculator for all cost components.
        """
        self.battery = battery
        self.cost_calculator = cost_calculator

    def run_step(self, power_kw: float, time_seconds: float, timestamp: datetime, cycle_number: int) -> dict:
        """
        Simulates a single time step.

        Args:
            power_kw (float): Charging power in kW.
            time_seconds (float): Duration in seconds.
            timestamp (datetime): Time of the charging action.
            cycle_number (int): Current cycle number.

        Returns:
            dict: {
                'new_soc': float,
                'electricity_cost': float,
                'calendar_ageing_cost': float,
                'cyclic_ageing_cost': float,
                'total_cost': float
            }
        """
        battery_capacity_kwh = self.battery.capacity_kwh
        current_soc = self.battery.soc

        electricity_cost = self.cost_calculator.get_electricity_cost(
            power_kw, time_seconds, timestamp
        )

        calendar_ageing_cost = self.cost_calculator.get_calendar_ageing_cost(
            current_soc, time_seconds
        )

        cyclic_ageing_cost = self.cost_calculator.get_cyclic_ageing_cost(
            power_kw, time_seconds, battery_capacity_kwh
        )

        # Update SOC
        self.battery.update_soc(power_kw, time_seconds)

        total_cost = electricity_cost + calendar_ageing_cost + cyclic_ageing_cost

        return {
            'new_soc': self.battery.soc,
            'electricity_cost': electricity_cost,
            'calendar_ageing_cost': calendar_ageing_cost,
            'cyclic_ageing_cost': cyclic_ageing_cost,
            'total_cost': total_cost
        }