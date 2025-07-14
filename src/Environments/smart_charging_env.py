import gymnasium as gym
from gymnasium import spaces
import numpy as np
from io import StringIO
from datetime import datetime, timedelta

from src.battery import Battery
from src.Models.price_model import PriceModel
from src.Models.degradation_model import DegradationModel
from src.cost_calculator import CostCalculator
from src.simulation_engine import SimulationEngine

class SmartChargingEnv(gym.Env):
    def __init__(self):
        super().__init__()

        # Define the discrete action space: 7 possible power values
        self.action_space = spaces.Discrete(7)  # Index maps to [-6, -4, -2, 0, 2, 4, 6]

        # Observation space: [SOC, time_step]
        low = np.array([0.0, 0])               # SOC can't go below 0, timestep can't be negative
        high = np.array([1.0, 95])             # SOC max 1.0, time index max 95 (15-min steps over 24h)

        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)
        self.initial_soc = 0.5
        self.target_soc = 0.9
        self.current_time_step = 0
        self.action_to_power = [-6, -4, -2, 0, 2, 4, 6]
        self.max_steps = 96 

        battery = Battery(capacity_kwh=46.0, initial_soc=self.initial_soc)

        # Dummy electricity price profile for 96 timesteps (15-minute intervals in 24 hours)
        start_time = datetime(2024, 1, 1, 0, 0)
        rows = []

        for i in range(96):
            ts_start = start_time + timedelta(minutes=15 * i)
            ts_end = ts_start + timedelta(minutes=15)
            rows.append(f"{ts_start.isoformat()},{ts_end.isoformat()},0.2")

        dummy_csv = StringIO("ts_start,ts_end,price\n" + "\n".join(rows))
        price_model = PriceModel(price_data_csv=dummy_csv.getvalue())

        # Dummy degradation model with simple linear cost mappings
        # Assuming: C-rates = [0.5, 2.0], costs = [2.0, 4.0] for interpolation test
        degradation_model = DegradationModel()  # Uses defaults

        cost_calculator = CostCalculator(
            price_model=price_model,
            degradation_model=degradation_model
        )
        self.engine = SimulationEngine(battery=battery, cost_calculator=cost_calculator)

    def step(self, action):
        power_kw = self.action_to_power[action]

        # Use timestamp if needed by pricing
        current_timestamp = datetime(2024, 1, 1) + timedelta(minutes=15 * self.current_time_step)
        cycle_number = 1

        # Run simulation step
        result = self.engine.run_step(power_kw, 15 * 60, current_timestamp, cycle_number)
        new_soc = result['new_soc']
        total_cost = result['total_cost']

        # Basic reward = negative cost
        reward = -total_cost

        # Advance time
        self.current_time_step += 1

        terminated = self.current_time_step >= self.max_steps
        truncated = False

        if terminated:
            soc_error = abs(new_soc - self.target_soc)
            penalty = soc_error * 50  # You can tune this multiplier
            reward -= penalty  # Larger penalty if final SOC is too far from target

        observation = np.array([new_soc, self.current_time_step], dtype=np.float32)
        info = {}

        return observation, reward, terminated, truncated, info

    def reset(self, seed=None, options=None):
        self.current_time_step = 0
        self.engine.battery.soc = self.initial_soc

        observation = np.array([self.engine.battery.soc, self.current_time_step], dtype=np.float32)
        return observation, {}


    def render(self):
        pass
