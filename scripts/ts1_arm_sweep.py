"""
KARA Test Script 1: Arm Sweep Motion

This script performs a simple arm sweep motion using the SO-101 model in MuJoCo.
It serves as a basic test of the simulation setup and can be used to verify that
the model is loaded correctly and that the joints can be controlled.
"""

import mujoco
import numpy as np

from kara.sim import sim_viewer, arm_model


def sweep_arm(model: mujoco.MjModel, data: mujoco.MjData) -> None:
    """
    Perform a simple arm sweep motion by controlling the first 6 joints.

    Args:
        model: The MuJoCo model object for the SO-101 arm.
        data: The MuJoCo data object for the SO-101 arm.
    """
    pose_a = np.zeros(6)  # Starting pose (all joints at 0)
    pose_b = np.array([-1, 1, -1, 1, -1, 1])

    # Sweep from pose_a to pose_b and back
    t = data.time  # Simulation time variable
    sweep_period = 5.0  # Time to complete one full sweep (A -> B -> A)
    alpha = 0.5 * (
        1 - np.cos(2 * np.pi * t / sweep_period)
    )  # Oscillates between 0 and 1
    target_pose = pose_a + alpha * (pose_b - pose_a)
    data.ctrl[:] = target_pose


if __name__ == "__main__":
    model, data = arm_model.load_arm_model()
    arm_model.print_joint_data(model)
    sim_viewer.launch_viewer(model, data, on_step_callback=sweep_arm)
    print("Arm sweep test complete.")
