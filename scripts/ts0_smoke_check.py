"""
KARA Test Script 0: Smoke Test

Load the SO-101 in MuJoCo (TheRobotStudio model).
"""

from kara.sim import sim_viewer, arm_model


def smoke_test():
    """
    Function to perform the smoke test by loading the
    SO-101 model and launching the MuJoCo viewer.
    """
    # Load the KaraArm sim model and create a MuJoCo data object
    kara_arm = arm_model.KaraArm()
    print(f"Model loaded: {kara_arm.model.nv} DOF, {kara_arm.model.nbody} bodies, {kara_arm.model.nu} actuators")

    # Print SO-101 joint information
    kara_arm.print_joint_data()

    # Launch the MuJoCo viewer to visualize the model
    sim_viewer.launch_viewer(kara_arm.model, kara_arm.data)


if __name__ == "__main__":
    smoke_test()
    print("Smoke test complete.")
