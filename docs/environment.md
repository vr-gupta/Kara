# KARA environment setup

This document is the reproduction recipe for KARA's development
environment. If you're a new contributor (or future-me on a new
machine), follow these steps end-to-end and you should land on a
working simulation.

## Prerequisites

- **OS:** macOS (Apple Silicon tested) or Linux. Windows may work
  but is untested.
- **Git** with sparse-checkout support (git >= 2.25).
- **A C toolchain** for building a couple of source-only Python
  packages (Xcode Command Line Tools on macOS, `build-essential`
  on Debian/Ubuntu).

## Python: use Homebrew (macOS) or system Python (Linux)

KARA uses MuJoCo's `mjpython` wrapper on macOS to run the passive
viewer. `mjpython` dlopens `libpython3.11.dylib` at runtime, which
means the Python interpreter must ship that shared library.

**uv's bundled standalone Python builds do NOT ship libpython as
a shared library**, so they don't work with `mjpython`. Use Homebrew
Python on macOS instead:

```bash
brew install python@3.11
# Verify the shared lib exists:
ls $(brew --prefix python@3.11)/Frameworks/Python.framework/Versions/3.11/lib/libpython3.11.dylib
```

On Linux, the distribution Python 3.11 (e.g. `apt install python3.11
python3.11-dev`) is fine — it ships libpython as a shared lib by
default.

## Install uv

uv is the Python project manager KARA uses for dependencies,
virtual environments, and lockfile-based reproducibility.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your shell (or `source ~/.zshrc` / `source ~/.bashrc`)
so `uv` is on your PATH.

## Clone the repo

```bash
git clone <your-kara-repo-url>
cd Kara
```

## Create the venv and install dependencies

Point uv at the Homebrew Python explicitly so it doesn't reach for
its own bundled build:

```bash
# macOS
uv venv --python $(brew --prefix python@3.11)/bin/python3.11

# Linux
uv venv --python $(which python3.11)
```

Then sync dependencies from the lockfile:

```bash
uv sync
```

The first `uv sync` on a fresh machine downloads ~700 MB of wheels
(torch, torchvision, opencv, rerun-sdk, etc.) and may take several
minutes. Subsequent syncs on the same machine are near-instant
because uv caches everything globally across projects.

> **Note:** do NOT run `uv add lerobot` from scratch on a fresh
> machine — that triggers a full universal lockfile resolve (18
> platform/Python combinations) which can take 15+ minutes.
> `uv sync` reads the existing lockfile and skips resolution.

## Fetch the SO-101 simulation model

KARA uses the official SO-101 MJCF from TheRobotStudio (the people
who designed the arm). It lives in a subfolder of the SO-ARM100
umbrella repo. We grab only that subfolder with a sparse-checkout
so we don't clone the whole repo:

```bash
mkdir -p sim/third_party
cd sim/third_party
git clone --depth 1 --filter=blob:none --sparse \
    https://github.com/TheRobotStudio/SO-ARM100.git
cd SO-ARM100
git sparse-checkout set Simulation/SO101
cd ../../..
```

You should now have
`sim/third_party/SO-ARM100/Simulation/SO101/scene.xml` and the
calibrated MJCF files alongside it.

This directory is in `.gitignore` — the model is a dependency, not
part of KARA's source, so we reconstruct it on setup rather than
vendoring it.

## Verify the install

Run the smoke test. On macOS, use `mjpython` (not plain `python`):

```bash
# macOS
uv run mjpython sim/smoke_check.py

# Linux
uv run python sim/smoke_check.py
```

Expected output:
- A line showing the path to `scene.xml`
- `Model loaded: 6 DOF, 8 bodies, 6 actuators`
- A list of joint names: shoulder_pan, shoulder_lift, elbow_flex,
  wrist_flex, wrist_roll, gripper
- A MuJoCo viewer window showing the SO-101 at home position

Close the viewer window to exit cleanly.

## Troubleshooting

**`mjpython` fails with `dlopen ... libpython3.11.dylib ... no such
file`.** Your venv is built against a Python that doesn't ship
libpython as a shared lib (likely uv's bundled standalone Python).
Rebuild the venv against Homebrew Python: `rm -rf .venv && uv venv
--python $(brew --prefix python@3.11)/bin/python3.11 && uv sync`.

**`launch_passive requires that the Python script be run under
mjpython on macOS`.** You ran the smoke test with plain `python`
on macOS. Use `uv run mjpython sim/smoke_check.py` instead.

**`No SO-101 MJCF found` / file not found error from smoke test.**
You skipped the sparse-checkout step. Re-run the "Fetch the SO-101
simulation model" section.

**`uv add` or `uv sync` is extremely slow (> 10 minutes with no
visible progress).** First, always run with `--verbose` so you can
see what's happening. If you're on a fresh machine with no cache,
the first sync genuinely takes a few minutes — be patient. If the
resolver is churning on "Selecting:" lines for more than 20
minutes, you've probably accidentally triggered a full resolve
instead of a sync; try `uv sync` (not `uv add` or `uv lock`).

**conda's `(base)` environment is interfering.** If your shell
prompt shows `(base)`, conda is auto-activating. Run `conda
deactivate` for this shell, and permanently disable auto-activation
with `conda config --set auto_activate_base false`. KARA does not
use conda.

**MuJoCo viewer opens but shows a black window / crashes on Mac.**
Usually an architecture mismatch (x86_64 Python running under
Rosetta trying to use arm64 MuJoCo, or vice versa). Verify with
`python -c "import platform; print(platform.machine())"` — it
should say `arm64` on Apple Silicon. If it says `x86_64`, your
Python is running under Rosetta; reinstall with a native arm64
Python.

## What's installed

After `uv sync` succeeds you have ~93 Python packages in `.venv/`.
The ones you'll interact with directly:

- **mujoco** — physics simulator
- **lerobot** — robot learning library (datasets, policies, hw)
- **torch / torchvision** — deep learning framework
- **numpy** — numerical arrays (the lingua franca)
- **opencv-python** — image processing
- **rerun-sdk** — robotics-specific visualization
- **feetech-servo-sdk** — Feetech STS3215 motor control (for the
  real arm in Month 3+)

The rest are transitive dependencies. Run `uv tree` to see the
full hierarchy.

## Updating dependencies

To update a single package:

```bash
uv add <package>@latest
```

To update everything within the version constraints in
`pyproject.toml`:

```bash
uv lock --upgrade
uv sync
```

Always commit the updated `uv.lock` afterward — that's how
reproducibility persists across the team.
