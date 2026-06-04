"""KARA smoke test: load the SO-101 in MuJoCo (TheRobotStudio model)."""
import pathlib
import time
import mujoco
import mujoco.viewer

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SCENE = REPO_ROOT / "sim" / "third_party" / "SO-ARM100" / "Simulation" / "SO101" / "scene.xml"


def main():
    if not SCENE.exists():
        raise SystemExit(
            f"Model not found at {SCENE}\n"
            "Run the sparse-checkout commands in docs/environment.md to fetch it."
        )

    print(f"Loading: {SCENE}")
    model = mujoco.MjModel.from_xml_path(str(SCENE))
    data = mujoco.MjData(model)
    print(f"Model loaded: {model.nq} DOF, {model.nbody} bodies, {model.nu} actuators")

    print("Joint names:")
    for i in range(model.njnt):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i)
        print(f"  [{i}] {name}")

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
    print("Viewer closed. Smoke test complete.")

if __name__ == "__main__":
    main()
