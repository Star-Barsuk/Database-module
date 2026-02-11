"""
Database configuration.
"""

from __future__ import annotations

import os

from .base import Config


class DatabaseConfig:
    """Database configuration manager."""

    def __init__(self, config: Config):
        self.config = config

    def _get_db_env_var(self, base_name: str, default: str = None) -> str:
        """Get database environment variable with environment suffix."""
        return self.config.get_env_var(base_name, default)

    @property
    def database_url(self) -> str:
        """Build database connection string."""
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = self._get_db_env_var("DB_NAME", "appdb")
        db_user = self._get_db_env_var("DB_USER", "appuser")
        db_password = self.config._secret_reader.read_secret("db_password")

        if not db_password:
            print("⚠️  Warning: No database password found in secrets")
            db_password = self._get_db_env_var("DB_PASSWORD", "")

        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    @property
    def database_url_safe(self) -> str:
        """Safe version for logging (without password)."""
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = self._get_db_env_var("DB_NAME", "appdb")
        db_user = self._get_db_env_var("DB_USER", "appuser")

        return f"postgresql://{db_user}:***@{db_host}:{db_port}/{db_name}"

    @property
    def pool_min_size(self) -> int:
        """Minimum connection pool size."""
        return int(os.getenv("DB_POOL_MIN_SIZE", "1"))

    @property
    def pool_max_size(self) -> int:
        """Maximum connection pool size."""
        return int(os.getenv("DB_POOL_MAX_SIZE", "20"))

    @property
    def connect_timeout(self) -> int:
        """Connection timeout in seconds."""
        return int(os.getenv("DB_CONNECT_TIMEOUT", "60"))
