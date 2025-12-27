import gymnasium as gym

# Create environment
env = gym.make("MountainCar-v0")

episodes = int(input("Enter number of episodes: "))

for ep in range(episodes):
    state, _ = env.reset()
    done = False

    while not done:
        action = env.action_space.sample()
        state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

print("Training completed")
env.close()
