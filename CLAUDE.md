# Repository guidance

For-fun robot learning experiments: behavior cloning now, pretrained VLA and
world models later. See README.md for setup and commands.

- Keep it simple. Add abstractions and experiment folders only when needed.
- Use `python -m robot_learning` or the installed `robot-learning` CLI.
- Use an editable install and the existing virtual environment; never hard-code
  an environment path. Default config: `robot_learning/configs/bin_sort.yaml`.
- Import shared utilities from `robot_learning.utils`; top-level `util` and
  `robot_learning/main.py` remain compatibility shims.
- Keep existing `outputs/robot_learning/` paths and checkpoint/data formats.
- Do not import research code from `mujoco_rl` or alter the robot submodule as
  part of routine learning changes.
- The local tray robot XML is intentional. The upstream robot has a push rod;
  it is not a replacement for this task's robot or controller.
- Keep Python 3.10+ syntax, float32 at torch boundaries, and frozen dataclasses
  for configuration. Developed with Python 3.12.
- The expert is open-loop and has known cube-placement failures. Structural
  changes must not silently retune physics, controller behavior, or policies.
- Historical debugging notes live in `docs/bin_sort_notes.md`; they are not
  the source of truth for current defaults or validated success rates.
