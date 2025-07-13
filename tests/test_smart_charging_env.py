import gymnasium as gym
import numpy as np
from src.Environments.smart_charging_env import SmartChargingEnv

def test_env_initialization():
    env = SmartChargingEnv()

    assert isinstance(env.action_space, gym.spaces.Discrete)
    assert env.action_space.n == 7

    assert isinstance(env.observation_space, gym.spaces.Box)
    assert env.observation_space.shape == (2,)
    assert (env.observation_space.low == [0.0, 0]).all()
    assert (env.observation_space.high == [1.0, 95]).all()

def test_env_reset():
    env = SmartChargingEnv()
    
    env.current_time_step = 10
    env.engine.battery.soc = 0.8
    
    observation, info = env.reset()
    
    expected_obs = np.array([env.initial_soc, 0], dtype=np.float32)

    assert np.array_equal(observation, expected_obs), "Reset observation mismatch"
    assert env.current_time_step == 0, "Current time step not reset"
    assert env.engine.battery.soc == env.initial_soc, "Battery SOC not reset"
    assert info == {}, "Info dict should be empty"

def test_env_step():
    env = SmartChargingEnv()
    observation, _ = env.reset()  

    # Check initial observation values
    assert np.allclose(observation, [0.5, 0])

    action = 6  # highest charging power index

    obs, reward, terminated, truncated, info = env.step(action)

    assert isinstance(obs, np.ndarray)
    assert obs.shape == (2,)
    assert obs[1] == 1  # timestep incremented by 1

    # Reward should be a float (negative cost)
    assert isinstance(reward, float)
    assert reward <= 0  # cost is positive, so reward is negative or zero

    # Episode should not be terminated after 1 step
    assert terminated is False

    # Truncated should be False as per your design
    assert truncated is False

    # Info dictionary should be empty
    assert info == {}