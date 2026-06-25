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
    # Load the SO-101 model and create a MuJoCo data object
    model, data = arm_model.load_arm_model()
    print(f"Model loaded: {model.nv} DOF, {model.nbody} bodies, {model.nu} actuators")

    # Print SO-101 joint information
    arm_model.print_joint_data(model)

    # Launch the MuJoCo viewer to visualize the model
    sim_viewer.launch_viewer(model, data)


if __name__ == "__main__":
    smoke_test()
    print("Smoke test complete.")
