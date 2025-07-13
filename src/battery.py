class Battery:

    def __init__(self, capacity_kwh, initial_soc = 0.0):
        self.capacity_kwh = capacity_kwh
        self.soc = initial_soc

    def update_soc(self, power_kw, time_seconds):
        """
        Updates the battery's state of charge (SOC) based on charging or discharging power and duration.

        The method calculates the energy change in kilowatt-hours (kWh) using the 
        formula: energy = power × time. It then updates the SOC accordingly, ensuring 
        the value is clamped between 0.0 (0%) and 1.0 (100%).

        Args:
            power_kw (float): Charging or discharging power in kilowatts (kW). 
            Use negative values for discharging.
            time_seconds (float): Duration of energy transfer in seconds.

        Returns:
            None
        """
        time_hours = time_seconds / 3600
        energy_added = power_kw * time_hours
        soc_change = energy_added / self.capacity_kwh
        self.soc = min(max(self.soc + soc_change, 0.0), 1.0)
