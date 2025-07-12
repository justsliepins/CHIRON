import math

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