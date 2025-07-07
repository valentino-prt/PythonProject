import os
from pathlib import Path

import yaml

CONFIG_FILE = Path(__file__).resolve().parents[1] / "config.yaml"
DEFAULT_ENV = "dev"

_env = os.getenv("MY_PROJECT_ENV", DEFAULT_ENV)

with open(CONFIG_FILE, "r") as f:
    _raw_config = yaml.safe_load(f)

if _env not in _raw_config:
    raise ValueError(f"Invalid env: {_env}")

config = _raw_config[_env]
