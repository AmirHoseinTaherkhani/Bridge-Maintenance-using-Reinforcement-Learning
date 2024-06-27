from typing import Callable
from stable_baselines3.common.callbacks import BaseCallback
import numpy as np

# Create a custom callback class
class EntropyCoefficientCallback(BaseCallback):
    def __init__(self, ent_coef_schedule: Callable, verbose=0):
        super(EntropyCoefficientCallback, self).__init__(verbose)
        self.ent_coef_schedule = ent_coef_schedule

    def _on_training_start(self) -> None:
        # Retrieve the PPO model and set the initial entropy coefficient
        self.model.ent_coef = self.ent_coef_schedule(0)

    def _on_step(self) -> bool:
        # Update the entropy coefficient based on the current timestep
        self.model.ent_coef = self.ent_coef_schedule(self.num_timesteps)
        return True

# create adaptive learning rate function
def adaptive_learning_rate_schedule(timestep):
    base_lr = 0.01
    min_reward = 1e-7
    scaling_factor = np.log10(min_reward)
    learning_rate = base_lr / (scaling_factor + timestep)  # Adjust timestep to control the adaptation speed
    return max(learning_rate, base_lr * 0.01)  # Minimum learning rate to prevent it from getting too small


# Define the entropy coefficient schedule
def ent_coef_schedule(timestep):
    initial_coef = 0.05
    final_coef = 0.0005
    total_timesteps = 1500000
    slope = (final_coef - initial_coef) / total_timesteps
    return max(initial_coef + slope * timestep, final_coef)