from datetime import datetime, timezone
import math
import numpy as np

class CostCalculator:
    def __init__(self, price_model, degradation_model=None):
        self.price_model = price_model
        self.degradation_model = degradation_model

    def get_electricity_cost(self, power_kw, time_seconds, timestamp):
        """
        Calculate the electricity cost for a charging/discharging action.

        Args:
            power_kw (float): Power in kW (positive for charging, negative for discharging).
            time_seconds (float): Duration in seconds.
            timestamp (datetime): Timestamp of the action.

        Returns:
            float: Cost in euros (€).
        """
        price_per_kwh = self.price_model.get_price(timestamp)
        time_hours = time_seconds / 3600
        energy_kwh = power_kw * time_hours
        cost = energy_kwh * price_per_kwh
        return cost

    def get_calendar_ageing_cost(self, soc: float, time_seconds: float) -> float:
        """
        Calculates calendar ageing cost based on SOC and time using piecewise
        linear interpolation on data from (You et al., 2024). Based on asumption
        that a 20% loss costs €8,000

        Args:
            soc (float): State of Charge (0 to 1).
            time_seconds (float): Time duration in seconds.

        Returns:
            float: Calendar ageing cost in euros (€).
        """
        soc_points = [0.0, 0.5, 1.0] # TODO: get more soc points
        cost_rates = [0.037, 0.092, 0.204]

        current_rate = np.interp(soc, soc_points, cost_rates)

        hours = time_seconds / 3600
        return current_rate * hours

    def get_sei_degradation_cost(self, cycle_number):
        """
        Calculate the SEI (Solid Electrolyte Interphase) degradation cost for a given cycle.

        This method uses the degradation model (if provided) to estimate the monetary cost
        of SEI film growth at a specific battery cycle number. The cost typically decreases
        with each subsequent cycle, modeled using an exponential decay function.

        Args:
            cycle_number (int): The current battery cycle number (starting from 1).

        Returns:
            float: Estimated SEI degradation cost in euros (€). Returns 0.0 if no degradation model is set.
        """
        if self.degradation_model:
            return self.degradation_model.get_sei_cost(cycle_number)
        return 0.0

    def get_cyclic_ageing_cost(self, power_kw: float, time_seconds: float, battery_capacity_kwh: float) -> float:
        """
        Calculate cyclic ageing cost for a charging event.

        Args:
            power_kw (float): Power during charging in kW.
            time_seconds (float): Duration in seconds.
            battery_capacity_kwh (float): Total battery capacity in kWh.

        Returns:
            float: Cyclic ageing cost in euros.
        """
        if not self.degradation_model:
            return 0.0
        
        c_rate = power_kw / battery_capacity_kwh

        time_hours = time_seconds / 3600
        energy_added_kwh = power_kw * time_hours
        cycle_portion = energy_added_kwh / battery_capacity_kwh

        return self.degradation_model.get_cyclic_cost(c_rate, cycle_portion)