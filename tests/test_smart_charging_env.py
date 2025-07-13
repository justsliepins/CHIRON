import gymnasium as gym
from src.Environments.smart_charging_env import SmartChargingEnv

def test_env_initialization():
    env = SmartChargingEnv()

    assert isinstance(env.action_space, gym.spaces.Discrete)
    assert env.action_space.n == 7

    assert isinstance(env.observation_space, gym.spaces.Box)
    assert env.observation_space.shape == (2,)
    assert (env.observation_space.low == [0.0, 0]).all()
    assert (env.observation_space.high == [1.0, 95]).all()
