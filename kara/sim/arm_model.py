"""
KARA Arm Model

This module provides utilities for loading and interacting
with the SO-101 arm model in MuJoCo.
"""

import mujoco
import numpy as np
import pathlib
from kara.sim import MODEL_SCENE_PATH_MAP, KaraArmSimModelType

from dataclasses import dataclass


@dataclass
class JointInfo:
    """
    Data class to hold information about a joint in the SO-101 arm model.
    """
    index: int
    name: str
    limited: bool
    range: np.ndarray
    target_position: float = 0.0
    actual_position: float = 0.0


class KaraArm:
    """
    Class to load and interact with Kara arm model in MuJoCo.
    """
    model_type: KaraArmSimModelType
    model: mujoco.MjModel
    data: mujoco.MjData
    joint_info_list: list[JointInfo]

    def __init__(self, model_type: KaraArmSimModelType = KaraArmSimModelType.SO101):
        """
        Initialize the KaraArm with the specified model.

        Args:
            model_type: The KaraArmModelType enum value specifying the arm model to load.
        """
        self.model_type = model_type
        if model_type in MODEL_SCENE_PATH_MAP:
            self.load_arm_model(MODEL_SCENE_PATH_MAP[model_type])
        else:
            raise ValueError(f"Unsupported KaraArm Sim Model: {model_type}")


    def load_arm_model(self, model_scene_path: pathlib.Path) -> None:
        """
        Load the SO-101 arm model from the specified scene XML file.

        Args:
            model_scene_path: The path to the scene XML file for the SO-101 arm.
        """
        if not model_scene_path.exists():
            raise FileNotFoundError(
                f"Model not found at {model_scene_path}. Please ensure the path is correct."
            )

        self.model = mujoco.MjModel.from_xml_path(str(model_scene_path))
        self.data = mujoco.MjData(self.model)
        self.joint_info_list = [
            JointInfo(
                index=i,
                name=mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_JOINT, i),
                limited=bool(self.model.jnt_limited[i]),
                range=self.model.jnt_range[i]
            )
            for i in range(self.model.njnt)
        ]

    def update_joint_positions(self) -> None:
        """
        Update the actual positions of all joints in the Kara arm model.
        """
        for joint_info in self.joint_info_list:
            qpos_addr = self.model.jnt_qposadr[joint_info.index]
            joint_info.actual_position = self.data.qpos[qpos_addr]

    def print_joint_data(self) -> None:
        """
        Print the indices, names, and the range of all joints in the model.
        """
        print("Idx | Joint Name              | Limited | Range (rad)")
        for joint_info in self.joint_info_list:
            if joint_info.limited:
                print(f"{joint_info.index:<3} | {joint_info.name:<23} | yes     | [{joint_info.range[0]:+.3f}, {joint_info.range[1]:+.3f}]")
            else:
                print(f"{joint_info.index:<3} | {joint_info.name:<23} | no      | (Unlimited)")

