import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from ppo2048 import Game2048,Game2048Env
from stable_baselines3.common.results_plotter import plot_results
from stable_baselines3.common import results_plotter
from stable_baselines3.common.monitor import Monitor
import os

now_path=os.path.dirname(os.path.abspath(__file__))
# Parallel environments

env = Monitor(Game2048Env(),now_path+'/monitor')
custom_objects = {"lr_schedule": None,'clip_range': lambda x: x,"Game2048Env":Game2048Env}
print("load...",now_path)
def evaluate_model(model, env, n_eval_episodes=10):
    rewards = []
    for i in range(n_eval_episodes):
        obs = env.reset()
        done = False
        episode_reward = 0
        while not done:
            action, _ = model.predict(obs)
            obs, reward, done, info = env.step(action)
            episode_reward += reward
        rewards.append(episode_reward)
    mean_reward = sum(rewards) / n_eval_episodes
    print(f"Mean reward: {mean_reward}")

# print(check_env(env))
# #訓練演算法
# model = PPO("MlpPolicy", env, verbose=1)
model = PPO.load(now_path+"/log/"+"ppo_cartpole",custom_objects = custom_objects,env=env,tensorboard_log=now_path+"/tb_logs/")
if model==None: 
    print("_____\nfail to load model\n_____")
model.learn(total_timesteps=100000)
model.save(now_path+"/log/"+"ppo_cartpole")


# Plot results
evaluate_model(model,env)
# mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
# print(f"Mean reward: {mean_reward:.2f} +/- {std_reward:.2f}")
# monitorF=results_plotter.load_results(now_path+"/monitor")
# print(monitorF)
# results_plotter.plot_curves([monitorF], x_axis=results_plotter.X_TIMESTEPS, title = "PPO")
# plot_results([now_path+"/monitor"],num_timesteps = None, x_axis=results_plotter.X_TIMESTEPS, task_name="PPO")


# del model # remove to demonstrate saving and loading
