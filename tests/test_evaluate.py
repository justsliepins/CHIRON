import os
from glob import glob
from src.Environments.smart_charging_env import SmartChargingEnv
from stable_baselines3 import DQN

def test_evaluate():
    # Find the latest saved model in the Agents/ folder
    model_files = glob("Agents/dqn_smart_charging_*.zip")
    if not model_files:
        raise FileNotFoundError("No trained models found in 'Agents/'.")

    # Sort by timestamp in filename and pick the latest
    latest_model_path = sorted(model_files)[-1]

    # Load the latest model
    print(f"Loading latest model: {latest_model_path}")
    model = DQN.load(latest_model_path)

    # Create the environment
    env = SmartChargingEnv()
    obs, info = env.reset()

    total_cost = 0
    for _ in range(96):  # Run for one full episode
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        total_cost -= reward  # Cost is the negative of the reward

        if terminated:
            break

    final_soc = env.engine.battery.soc * 100
    print(f"\nEvaluation Complete!")
    print(f"Final SOC: {final_soc:.2f}%")
    print(f"Total Cost: €{total_cost:.2f}")
