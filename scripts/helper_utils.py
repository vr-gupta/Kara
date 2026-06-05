"""
Helper utilities for the KARA project.

This module contains various utility functions and classes that are used
throughout the KARA project to simplify common tasks and improve code
readability and maintainability.
"""

import pathlib
import time
import mujoco
import mujoco.viewer

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SCENE = REPO_ROOT / "sim" / "third_party" / "SO-ARM100" / "Simulation" / "SO101" / "scene.xml"

def load_model() -> tuple[mujoco.MjModel, mujoco.MjData]:
    """Load the SO-101 model from the specified XML file."""
    if not SCENE.exists():
        raise SystemExit(
            f"Model not found at {SCENE}\n"
            "Run the sparse-checkout commands in docs/environment.md to fetch it."
        )

    print(f"Loading: {SCENE}")
    model = mujoco.MjModel.from_xml_path(str(SCENE))
    data = mujoco.MjData(model)
    print(f"Model loaded: {model.nv} DOF, {model.nbody} bodies, {model.nu} actuators")
    return model, data

def print_joint_data(model: mujoco.MjModel):
    """Print the names of all joints in the model."""
    print("=============== Joint Data ===============")
    print("Index |\t\tJoint Name\t| Range of Motion")
    model_ranges = model.actuator_ctrlrange

    for i in range(model.njnt):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i)
        print(f"{i:<5} | {name:<23} | {model_ranges[i]}")

def run_viewer(model: mujoco.MjModel, data: mujoco.MjData):
    """Launch the MuJoCo viewer and run the simulation until the window is closed."""
    print("\nOpening viewer. Close the window to exit.")
    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            start_time = time.perf_counter()
            mujoco.mj_step(model, data)
            viewer.sync()
            elapsed = time.perf_counter() - start_time

            dt = model.opt.timestep
            sleep_time = max(0, dt - elapsed)
            time.sleep(sleep_time)
    print("Viewer closed.")
