"""
Base configuration module.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from .security import SecretReader


class Config:
    """Application configuration base class."""

    def __init__(self, env: str | None = None):
        self.env = env or self._detect_env()

        self._secret_reader = SecretReader()
        self._load_env_file()

    def get_env_var(self, base_name: str, default: str = None) -> str:
        """
        Get environment variable with environment-specific suffix.
        Tries: VAR_{SUFFIX}, VAR, then default.
        """
        suffixed_name = f"{base_name}_{self._env_suffix}"
        suffixed_value = os.getenv(suffixed_name)

        if suffixed_value is not None:
            return suffixed_value

        base_value = os.getenv(base_name)
        if base_value is not None:
            return base_value

        return default or ""

    def _load_env_file(self):
        """Load appropriate .env file."""
        project_root = Path(__file__).parent.parent.parent
        env_files = [
            # project_root / f"envs/.env.{self.env}",
            project_root / "envs/.env",
        ]

        for env_file in env_files:
            if env_file.exists():
                load_dotenv(env_file, override=True)
                print(f"📁 Loaded environment from: {env_file.name}")
                break

    def _detect_env(self) -> str:
        """Detect current environment."""
        active_env_file = Path(__file__).parent.parent.parent / ".active-env"
        if active_env_file.exists():
            with open(active_env_file) as f:
                return f.read().strip()

    @property
    def _env_suffix(self) -> str:
        """Get environment-specific suffix for variable names."""
        env_suffix_map = {
            "local": "LOCAL",
            "dev": "DEV",
            "prod": "PROD",
            "test": "TEST",
        }

        suffix = env_suffix_map.get(self.env, self.env.upper())
        print(f"📋 Environment suffix: {suffix}")
        return suffix

    @property
    def is_docker(self) -> bool:
        """Check if running inside Docker."""
        return Path("/.dockerenv").exists() or os.getenv("DOCKER_CONTAINER") == "true"

    @property
    def heartbeat_interval(self) -> int:
        """Get heartbeat interval in seconds."""
        return int(os.getenv("HEARTBEAT_INTERVAL", "5"))
