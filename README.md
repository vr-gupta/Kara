# KARA

KARA (कर — "hand" or "to-do" in Sanskrit) is a benchtop manipulation project
exploring foundation-model-driven learned policies on self-built
hardware. Built in the open as a learning journey toward the next
generation of intelligent physical products.

## What it does (planned)
A small SO-101 robot arm performs benchtop manipulation tasks (e.g.,
moving small objects between physical locations) using learned policies
trained in simulation and deployed to real hardware, orchestrated by a
vision-language model that interprets natural-language commands.

## Status
Day 0: environment set up, simulation working, hardware on order.

## Stack
- Hardware: SO-101 arm (TheRobotStudio open-source design),
  Feetech STS3215 servos
- Simulation: MuJoCo via the official SO-101 MJCF
- ML: LeRobot (imitation learning, ACT/Diffusion Policy)
- Language: Python 3.11, managed with uv

## Quickstart
See `docs/environment.md` for setup. The short version:
1. Install Homebrew Python 3.11 (macOS) or system Python 3.11 (Linux).
2. `uv sync` to install dependencies.
3. Clone the SO-101 sim model into `assets/robots/` (see env doc).
4. `uv run mjpython scripts/ts0_smoke_check.py` (macOS) to verify the sim loads.

## Structure
- `hardware/` — CAD, BOM, wiring, build notes
- `firmware/` — servo controller firmware
- `assets/` — MuJoCo models for the robots (just SO-101 for now)
- `kara/` — main Python package (perception, policy, control,
  telemetry, vlm)
- `scripts/` — training, eval, demo runners
- `docs/` — design docs, build guides, blog drafts
- `BUILD_LOG.md` — daily build journal

## License
MIT License
