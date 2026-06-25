"""
KARA Arm Model

This module provides utilities for loading and interacting
with the SO-101 arm model in MuJoCo.
"""

import mujoco
from kara.sim import SCENE


def load_arm_model() -> tuple[mujoco.MjModel, mujoco.MjData]:
    """
    Load the SO-101 arm model from the specified scene XML file.

    Returns:
        A tuple containing the MuJoCo model and data objects for the SO-101 arm.
    """
    if not SCENE.exists():
        raise FileNotFoundError(
            f"Model not found at {SCENE}. Please ensure the path is correct."
        )

    model = mujoco.MjModel.from_xml_path(str(SCENE))
    data = mujoco.MjData(model)
    return model, data


def print_joint_data(model: mujoco.MjModel) -> None:
    """
    Print the indices, names, and the range of all joints in the model.

    Args:
        model: The MuJoCo model object for the SO-101 arm.
    """
    print("Idx | Joint Name              | Limited | Range (rad)")
    for i in range(model.njnt):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i)
        limited = bool(model.jnt_limited[i])
        rng = model.jnt_range[i]
        if limited:
            print(f"{i:<3} | {name:<23} | yes     | [{rng[0]:+.3f}, {rng[1]:+.3f}]")
        else:
            print(f"{i:<3} | {name:<23} | no      | (Unlimited)")
