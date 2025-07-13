import math
import numpy as np

class DegradationModel:
    def __init__(self, initial_cost=6.088, decay_rate=0.013):
        """
        Initializes the degradation model with calibrated parameters.

        Args:
            initial_cost (float): The monetary cost (€) of SEI degradation
                                  for the first cycle. Derived from the 20mAh
                                  capacity loss reported in (You et al., 2024).
            decay_rate (float): The exponential decay rate, calibrated to match
                                the 1.5mAh capacity loss at cycle 200
                                (You et al., 2024).

        Note:
            For a full derivation of these default values, see the file:
            'root/docs/degradation_model_justification.md'
        """
        self.initial_cost = initial_cost
        self.decay_rate = decay_rate

    def get_sei_cost(self, cycle_number):
        """
        Calculate SEI film degradation cost based on cycle number using exponential decay.

        Args:
            cycle_number (int): Current cycle number.

        Returns:
            float: Degradation cost in euros.
        """
        return self.initial_cost * math.exp(-self.decay_rate * (cycle_number - 1))

    #TODO: add more c-rate points. Implement translator that takes ev parameters 
    # and charging speed and translate it to c-rate
    def get_cyclic_cost(self, c_rate: float, cycle_portion: float) -> float:
        """
        Calculate cyclic ageing cost based on C-rate and fraction of full cycle.

        Args:
            c_rate (float): Charging C-rate (e.g., 1.25 means 1.25C).
            cycle_portion (float): Fraction of full cycle (0 to 1).

        Returns:
            float: Cyclic ageing cost in euros.
        """
        # C-rate points and corresponding costs per full cycle (€)
        c_rate_points = [0.5, 2.0]
        cost_rates = [2.00, 4.00]

        cost_per_full_cycle = np.interp(c_rate, c_rate_points, cost_rates)

        return cost_per_full_cycle * cycle_portion