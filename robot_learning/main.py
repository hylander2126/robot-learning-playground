"""Compatibility entry point; prefer python -m robot_learning."""
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from robot_learning.cli import load_config, main, parse_args  # noqa: F401,E402

if __name__ == "__main__":
    main()
