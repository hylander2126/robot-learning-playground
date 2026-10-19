# Robot Learning Playground

Small, for-fun robot learning experiments in MuJoCo. The current task is an ABB
IRB120 sorting colored cubes from a tray into bins.

- **Behavior cloning:** state-only and goal-conditioned baselines, collection,
  training, evaluation, and diagnostics.
- **VLA:** a tiny image/language/state policy exists for experimentation;
  pretrained VLA fine-tuning is a future project.
- **World models:** planned; no implementation yet.

This project is independent of the research repo it came from. The robot assets
and math helpers come from the `mujoco_irb120` submodule.

## Setup

Clone your GitHub repo with `git clone --recurse-submodules <repo-url>`, or initialize
an existing checkout with `git submodule update --init --recursive`.
Use Python 3.10+ (developed on 3.12) and your preferred virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m robot_learning --help
```

Use an **editable install**: scene generation uses meshes from the submodule in
this checkout. A standalone wheel is not a supported distribution. Installing
PyTorch separately first lets you choose the build suitable for your machine.

## Run

From the checkout root, after activating your environment:

```bash
python -m robot_learning collect --episodes 5 --seed 0
python -m robot_learning train --policy-type goal_conditioned
python -m robot_learning eval \
  --checkpoint outputs/robot_learning/checkpoints/goal_conditioned_bc_best.pt
python -m robot_learning plot \
  --checkpoint outputs/robot_learning/checkpoints/goal_conditioned_bc.pt
python -m robot_learning diagnose \
  --checkpoint outputs/robot_learning/checkpoints/goal_conditioned_bc_best.pt
```

`robot-learning` is the same CLI after installation. Each subcommand has `--help`.
Select a config with `python -m robot_learning --config <path> collect ...`.
Defaults live in [bin_sort.yaml](robot_learning/configs/bin_sort.yaml).
Use `--policy-type state_only` or `--policy-type vla` to train the other policies.
Evaluation uses `--render` to save MP4s; headless Linux rendering may require
`MUJOCO_GL=egl` (GPU) or `MUJOCO_GL=osmesa` (CPU), with the corresponding system
libraries installed.

Datasets, checkpoints, videos, figures, and debug traces stay under
`outputs/robot_learning/`, which is ignored by Git. Existing files and paths are
preserved. Relative dataset/checkpoint paths resolve against the checkout root.
The legacy `python robot_learning/main.py ...` command and `util.*` imports still
work; new code should use the package CLI and `robot_learning.utils`.

## Layout

```text
robot_learning/
  cli.py                 collect / train / eval / diagnose / plot
  configs/bin_sort.yaml  experiment defaults
  environment/           simulation and scene generation
  assets/                tray robot and task XML
  experts/bin_sort.py    scripted demonstration policy
  task.py                bin-sort task specification
  controller.py          robot control and kinematics
  models/                BC and tiny VLA policies
  scripts/               collection, training, and evaluation workflows
  utils/                 paths, HDF5 datasets, runtime, debug logs
mujoco_irb120/            shared robot submodule (upstream project)
docs/bin_sort_notes.md    historical experiment and debugging notes
outputs/                 local generated artifacts (ignored)
```

Keep new experiments small: add models and scripts when needed, reuse the
simulation and data utilities, and introduce a new task folder when a second
task actually exists. No framework or placeholder packages are required.

## Current limits

The scripted expert and learned policies are experimental. Expert cube placement
has been unreliable; validate demonstrations before a long collection/training
run. No success-rate target in the historical notes is a guaranteed result.
The tiny VLA is trained locally with BC, not a pretrained VLA pipeline.
See [experiment notes](docs/bin_sort_notes.md) for past results and failure modes.

The suggested GitHub repository name is `robot-learning-playground`. Renaming the
checkout or GitHub repository does not change imports or artifact paths.

## Checks

With the project dependencies installed:

```bash
python -m unittest discover -s tests -v
```

These smoke tests cover CLI collection dispatch, compatibility imports, asset
paths, simulation reset/step, and the three policy interfaces. They do not
validate expert success or replace an end-to-end collection/training run.
