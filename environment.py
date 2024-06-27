import numpy as np
import pandas as pd
import gym
import time
from gym import spaces


#Define the environment
class BridgeEnv(gym.Env):
    
    def __init__(self, dataframe):
        super(BridgeEnv, self).__init__()
        '''Initialization parameters'''
        self.n_bridges = 19
        self.n_ratings = 9
        self.n_actions = 20
        self.bridges = dataframe
        self.ratings = self.bridges['Current_rating'].values
        
        
        # Defining Action Space
        self.action_space = spaces.Discrete(self.n_actions)

        # Defining State Space
        self.observation_space = spaces.Box(low=1, high=9, shape=(self.n_bridges,), dtype=np.float64)
        self.bridge_ratings = self.ratings

        self.current_year = 1
        self.horizon = 20
        self.reward = 0.0
        self.history = []
        # self.flood = 0


    def deterioration(self):
        '''This function accepts the current rating and the time for future rating and returns the future rating'''
       
        # Flood deterioration for each 6 months
        depth_10 = (self.bridge_ratings - self.bridges['Depth10_Rating'])/(2*10)
        depth_10 = depth_10 * (depth_10 > 0)
        
        depth_50 = (self.bridge_ratings - self.bridges['Depth50_Rating'])/(2*50)
        depth_50 = depth_50 * (depth_50 > 0)
        
        depth_100 = (self.bridge_ratings - self.bridges['Depth100_Rating'])/(2*100)
        depth_100 = depth_100 * (depth_100 > 0)
        
        depth_500 = (self.bridge_ratings - self.bridges['Depth500_Rating'])/(2*500)
        depth_500 = depth_500 * (depth_500 > 0)
        
        flood_deterioration = depth_10 + depth_50 + depth_100 + depth_500
        self.bridge_ratings = self.bridge_ratings - flood_deterioration

        #self.bridge_ratings = np.maximum(min_ratings, self.bridge_ratings - flood_deterioration)
        
        # Time deterioration for each 6 months
        time = 0.5
        t = (.046437526 - np.sqrt(.046437526**2-4*(- 0.000236059)*(9-self.bridge_ratings)))/(2 * -0.000236059)
        updated_rating = (9 - .046437526 * (t + time) - 0.000236059 * (t + time)**2)
        
        return np.abs(updated_rating)
####################################################################################################    
    def rating_cost_calculator(self, rnd, prob, cost):
        if rnd <= prob:
            return cost
        else:
            return 0    
####################################################################################################    
    #BElOW IS the Deterministic ENV
    def collapse_cost(self):
        '''This function will return the cost of failure and updated rating of the bridges'''
        
        """THE WHOLE THING SHOULD CHANGE"""
        #Get the total cost
        self.flood = 0
        cost = []
        i = 0
        
        for rate_ in self.bridge_ratings:
            cost.append(self.bridges['FailureCost_Rating' + str(int(np.round(rate_)))][i])
            i += 1
        Total_Cost = np.sum(np.array(cost))       
            
        return self.bridge_ratings, Total_Cost

    ####################################################################################################    
    def step(self, action):
        '''This is the step function of the environment; it takes an action and applies it on the environment'''
#         print(f'-----------------------Year {self.current_year} starts-----------------------')
#         print(self.bridge_ratings)
#         action_idx = action
        self.reward = 0
        action_cost = 0
        failure_cost = 0
        
        done = False
#         print(f'Previous Rating: {np.array(self.bridge_ratings)}')


        #Applying bridge deterioration
                
#         self.bridge_ratings = np.round(pseudo).astype(np.int32)
        

    
        
        # Perform the action and update the bridge ratings
#         print(f'Actions are {action}')

        bridge_idx = action


        #Conducting flood simulation
        self.bridge_ratings, failure_cost = self.collapse_cost()
        self.bridge_ratings = self.deterioration()

        if action == self.n_bridges:

                    # do nothing
            pseudo_cost  = 0
    #                 print(f'Do Nothing')

        elif action != self.n_bridges:
                    # repair
    #                 print(f'Repair Bridge {bridge_idx}')
            current_rating = int(np.round(np.array(self.bridge_ratings, dtype = np.float32)[bridge_idx]))    
            pseudo = np.array(self.bridge_ratings)
            pseudo[bridge_idx] = max(7, current_rating)
            self.bridge_ratings = pseudo

            pseudo_cost = self.bridges['cost_repair_rating' + str(abs(current_rating))][bridge_idx]
            if current_rating >= 7:
                pseudo_cost = 1000000
            action_cost += pseudo_cost

            
#       self.reward = self.reward -(action_cost + failure_cost)
        self.reward = -(action_cost + failure_cost)
        
        if self.current_year == self.horizon:
            #             self.endyear.append(self.horizon)
            done = True

            
#         self.total_repair_cost += action_cost + failure_cost
        self.history.append([self.bridge_ratings, action, self.reward, self.flood, self.current_year,\
                             action_cost, failure_cost])
        self.current_year += 1
        #         print(f'Action Cost = {action_cost}')
#         print(f'Failure Cost = {failure_cost}')
#         print(f'Total cost = {self.total_repair_cost}')
#         print(f'Updated Rating: {np.array(self.bridge_ratings)}')
#         print(f'-----------------------Year ends-----------------------')
        return self.bridge_ratings, float(self.reward), done, {}

   ####################################################################################################    
    def reset(self):
#         print('****************************************ENV RESETED****************************************')
        
        self.bridge_ratings = self.ratings
        self.reward = 0.0
        self.current_year = 1
        self.flood = 0
        self.total_repair_cost = 0 
        return self.bridge_ratings


