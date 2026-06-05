"""
KARA Test Script 1

This script performs a simple arm sweep motion using the SO-101 model in MuJoCo.
It serves as a basic test of the simulation setup and can be used to verify that
the model is loaded correctly and that the joints can be controlled.

"""

import numpy as np

from helper_utils import load_model, print_joint_data, run_viewer

def sweep_arm(data):
    """
    Perform a simple arm sweep motion by controlling the first 6 joints.
    """

    target_angles = np.array([-1, 1, -1, 1, -1, 1])
    data.ctrl[:6] = target_angles


if __name__ == "__main__":
    model, data = load_model()
    print_joint_data(model)
    sweep_arm(data)
    run_viewer(model, data)
