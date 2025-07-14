import os
from datetime import datetime
from src.Environments.smart_charging_env import SmartChargingEnv
from stable_baselines3 import DQN

def main():
    env = SmartChargingEnv()
    model = DQN("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=1000)

    os.makedirs("Agents", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f"Agents/dqn_smart_charging_{timestamp}"

    model.save(model_filename)

    print("✅ Smoke test complete! Training ran without errors.")

if __name__ == "__main__":
    main()
