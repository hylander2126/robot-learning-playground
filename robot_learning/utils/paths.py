from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = REPO_ROOT / "outputs"
ROBOT_LEARNING_OUTPUTS = OUTPUT_ROOT / "robot_learning"


def resolve_repo_path(path: str | Path) -> Path:
    """Resolve `path` against the repo root if it isn't already absolute."""
    path = Path(path)
    return path if path.is_absolute() else REPO_ROOT / path
