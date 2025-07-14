import numpy as np
from src.Environments.smart_charging_env import SmartChargingEnv

def test_final_soc_penalty():
    env = SmartChargingEnv()
    env.reset()
    env.target_soc = 0.9  # Make sure test uses this

    env.current_time_step = env.max_steps - 1  # One step before done
    env.engine.battery.soc = 0.6  # Too low

    _, reward, terminated, _, _ = env.step(action=3)  # action=3 corresponds to 0 kW

    assert terminated == True, "Episode should be terminated after final step"
    assert reward < -1.0, "Expected a large penalty for missing final SOC target"
