from datetime import datetime, timezone
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

    def get_calendar_ageing_cost(self, soc, time_seconds):
        """
        Calculates the calendar ageing cost based on SOC and elapsed time.

        Assumes a simple linear ageing cost rate of €0.10 per hour at 100% SOC.

        Args:
            soc (float): State of charge (0 to 1).
            time_seconds (float): Duration in seconds.

        Returns:
            float: Ageing cost in euros (€).
        """
        cost_rate = 0.10 
        time_hours = time_seconds / 3600
        cost = cost_rate * soc * time_hours
        return cost

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