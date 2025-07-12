from datetime import datetime, timezone
class CostCalculator:
    def __init__(self, price_model):
        self.price_model = price_model

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
        cost_rate = 0.10 #cost rate per hour at full soc
        time_hours = time_seconds / 3600
        cost = cost_rate * soc * time_hours
        return cost
