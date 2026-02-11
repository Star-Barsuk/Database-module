"""
Secret reading utilities.
"""

from __future__ import annotations

import os
from pathlib import Path


class SecretReader:
    """Handles reading secrets from various sources."""

    def __init__(self, project_root: Path | None = None):
        self.project_root = project_root or Path(__file__).parent.parent.parent

    def read_secret(self, secret_name: str, default: str | None = None) -> str:
        docker_path = Path(f"/run/secrets/{secret_name}")
        if docker_path.exists():
            content = self._read_file(docker_path)
            print(f"Secret {secret_name} read from docker: {len(content)} chars")
            return content

        local_path = self.project_root / f"docker/secrets/{secret_name}.txt"
        if local_path.exists():
            content = self._read_file(local_path)
            print(f"Secret {secret_name} read from local file: {len(content)} chars")
            return content

        env_value = os.getenv(secret_name.upper(), default or "")
        print(f"Secret {secret_name} from env: '{env_value[:8]}...' ({len(env_value)} chars)")
        return env_value

    def _read_file(self, file_path: Path) -> str:
        """Read and sanitize file content."""
        try:
            with open(file_path) as f:
                return f.read().strip()
        except OSError:
            return ""
