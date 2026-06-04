# KARA Build Log

## Day 0 — KARA begins (2026-04-09)

The first day of the project. The goals were modest: order hardware,
create the repo, set up a Python environment, and get the SO-101
loading in MuJoCo. Most of those things happened. Some of them took
much longer than expected.

### What I did
- Ordered the SO-101 BOM from AliExpress and a few local Singapore
  suppliers: 6× Feetech STS3215 servos, Waveshare bus driver board,
  12V power supply, M3 hardware kit. Estimated arrival ~10 days.
- Started 3D printing the SO-101 frame parts (PLA on a Bambu/Prusa,
  ~30 hours of print time across the batch).
- Created the kara repo on GitHub with a clean directory structure
  for hardware, firmware, sim, the Python package (perception,
  policy, control, telemetry, vlm), scripts, configs, and docs.
- Set up a Python 3.11 environment with uv. Installed lerobot,
  mujoco, numpy, opencv-python, pyyaml, rich, pytest. uv pulled
  in the full transitive ML stack including torch, torchvision,
  torchcodec, datasets, diffusers, accelerate, wandb, rerun-sdk —
  93 packages total, ~700 MB on disk.
- Fetched the official SO-101 MuJoCo model from TheRobotStudio's
  SO-ARM100 repo using a sparse-checkout, so only the
  Simulation/SO101 folder lives in third_party/.
- Wrote a smoke test (sim/smoke_test.py) that loads the SO-101
  scene, prints joint names and DOF count, and opens the MuJoCo
  passive viewer.
- Successfully ran the smoke test. The arm appeared in the viewer
  with all 6 joints (shoulder_pan, shoulder_lift, elbow_flex,
  wrist_flex, wrist_roll, gripper) at home position.

### What surprised me
- uv's dependency resolve for the lerobot stack took ~15 minutes,
  not because of slow downloads but because uv builds a *universal*
  lockfile across 18 platform/Python combinations. This is a one-
  time cost; future `uv sync` calls will take seconds.
- The first time I tried this through Claude Code, it ran for over
  100 minutes without producing visible progress. It turned out CC
  was working in an isolated git worktree under .claude/worktrees/,
  while I was looking at the main repo for evidence. It had also
  inherited my shell's conda `(base)` environment, which probably
  added confusion. I bailed out and ran the install in a plain
  terminal with `--verbose`, where progress was finally visible.
- lerobot does not ship the SO-101 MJCF in its pip package. Robot
  model files live in the hardware project's repo, not the ML
  library's package. I initially tried mujoco_menagerie's SO-ARM100
  as a substitute, then found the actual SO-101 model in
  TheRobotStudio/SO-ARM100/Simulation/SO101 — strictly better
  because it matches the physical hardware I'm building.
- mjpython is required on macOS for MuJoCo's passive viewer, and
  it doesn't work with uv's bundled standalone Python builds
  because they're statically linked and don't ship libpython3.11.dylib
  as a shared lib. The fix was to rebuild the venv against
  Homebrew's Python 3.11, which does ship the dylib. Took ~5 minutes
  once I knew the cause.

### What I learned
- uv is much faster than pip but its first resolve on a complex
  project is genuinely slow. Trust the process and use --verbose.
- Claude Code is great for writing code but the wrong tool for
  long-running installs where the value is in watching streaming
  output. Use a plain terminal for that.
- For robotics projects, hardware files, software, and ML assets
  all live in different repos and have to be wired up explicitly.
  Assume nothing about what's bundled where.
- macOS GUI applications (like the MuJoCo viewer) need to run on
  the main thread of a Cocoa-aware process. MuJoCo handles this
  with the `mjpython` wrapper, which has its own constraints on
  how the Python interpreter is built. Worth remembering for any
  future GUI-from-Python work.

### Time spent
- Hardware ordering and print setup: ~45 min
- Repo creation and structure: ~15 min
- Environment setup (including the failed Claude Code run, the
  retry, and the mjpython detour): ~3.5 hours
- Total: ~4.5 hours

### What's next (Day 1)
Make the simulated arm move under my own code. Write a script
that sends a joint trajectory to the SO-101 in MuJoCo and moves
it from home to a target pose and back, smoothly, while the
viewer is running. End-of-day artifact: a 5-second video of the
arm doing a clean sweep, committed to the repo as
sim/scripts/day1_sweep.py.
