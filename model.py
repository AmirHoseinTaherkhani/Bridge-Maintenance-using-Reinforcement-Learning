# %%
import numpy as np
import pandas as pd
import gym
import time
from gym import spaces
from environment import BridgeEnv
from utils import *
import stable_baselines3
from stable_baselines3.ppo import PPO
from stable_baselines3.ppo.policies import MlpPolicy
from stable_baselines3.common.callbacks import BaseCallback
from typing import Callable



#Read the file
df = pd.read_excel('Ratings.xlsx',
                   sheet_name='Alpha0')
#Sheet2 --> Authentic; Sheet3 --> Manipulated
# prob_of_failure = pd.read_excel('Ratings.xlsx', sheet_name='Sheet2')

#run the model
start = time.time()



# Create the environment
env = BridgeEnv(df)

# Policy Design
policy_kwargs = dict(net_arch=[64, 64, 64])

# Define the model
model = PPO(MlpPolicy, env, verbose=1, n_epochs=2000, ent_coef=0.01, learning_rate=adaptive_learning_rate_schedule)


# Create the callback object
callback = EntropyCoefficientCallback(ent_coef_schedule)

# Train the model with the callback
model.learn(total_timesteps=8000000, callback=callback)

end = time.time()
# Save the trained model
model.save('Models/model.json')


obs=[]
actions=[]
rewards=[]
flood=[]
current_year = []
action_cost=[]
failure_cost=[]
for i in range(len(env.history)):
    obs.append(env.history[i][0])
    actions.append(env.history[i][1])
    rewards.append(env.history[i][2])
    flood.append(env.history[i][3])
    current_year.append(env.history[i][4])
    action_cost.append(env.history[i][5])
    failure_cost.append(env.history[i][6])
results = pd.DataFrame({'observation': obs, 'actions': actions, 'rewards': rewards, 'flood': flood,\
                        'year': current_year, 'action_cost':action_cost, 'failure_cost': failure_cost})
results.to_csv('Results.csv')


episode_reward = []
for i in range(80000):
    episode_reward.append(np.average(np.array(results['rewards'][i*100:(i+1) * 100])))
episode_reward_df = pd.DataFrame(episode_reward)

results.iloc[np.argmax(episode_reward)*100:(np.argmax(episode_reward)+1)*100]\
.to_csv('BestPerformance.csv')


with open('time.txt', 'w') as f:
    f.write('total time  = ' + str(end-start)) 
# %%
