from src.Environments.smart_charging_env import SmartChargingEnv
from stable_baselines3 import DQN

def main():
    env = SmartChargingEnv()
    model = DQN("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=1000)

    print("✅ Smoke test complete! Training ran without errors.")

if __name__ == "__main__":
    main()
