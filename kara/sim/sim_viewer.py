"""
KARA Simulation Viewer

This module provides utilities for running a MuJoCo viewer
to visualize the simulation. It includes function to run
the viewer with an optional callback for each simulation step.
"""

import time
import mujoco


def launch_viewer(
    model: mujoco.MjModel, data: mujoco.MjData, on_step_callback=None
) -> None:
    """
    Launch the MuJoCo viewer and run the simulation until the window is closed.

    Args:
        model: The MuJoCo model object.
        data: The MuJoCo data object.
        on_step_callback: Optional callback function to be called at each simulation step.
    """
    print("\nOpening SimViewer. Close the window to exit.")
    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            start_time = time.perf_counter()
            mujoco.mj_step(model, data)

            if on_step_callback is not None:
                on_step_callback(model, data)

            viewer.sync()
            elapsed = time.perf_counter() - start_time

            dt = model.opt.timestep
            sleep_time = max(0, dt - elapsed)
            time.sleep(sleep_time)
    print("SimViewer closed.")
