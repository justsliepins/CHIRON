class Battery:

    def __init__(self, capacity_kwh, current_soc):
        self.capacity_kwh = capacity_kwh
        self.current_soc = current_soc

    def update_soc(self, power_kw, time_seconds):
        """
        Updates the battery's state of charge (SOC) based on charging power and duration.

        The method calculates the energy added in kilowatt-hours (kWh) using the 
        formula: energy = power × time. It then updates the SOC accordingly, ensuring 
        the value does not exceed 1.0 (100%).

        Args:
            power_kw (float): Charging power in kilowatts (kW).
            time_seconds (float): Duration of charging in seconds.

        Returns:
            None
        """
        one_hour_in_seconds = 3600
        time_hours = time_seconds / one_hour_in_seconds
        energy_added = power_kw * time_hours
        soc_change = energy_added / self.capacity_kwh
        self.current_soc += soc_change

        if self.current_soc > 1:
            self.current_soc = 1
