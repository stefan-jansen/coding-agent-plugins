"""
Configuration loading for references plugin.

Priority:
1. Project .env file (highest priority)
2. Environment variables
3. Built-in defaults
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Config:
    """Reference plugin configuration."""

    # Required
    refs_dir: Path
    zotero_library_id: int

    # Optional with defaults
    zotero_db: Path = field(default_factory=lambda: Path.home() / "Zotero" / "zotero.sqlite")
    zotero_storage: Path = field(default_factory=lambda: Path.home() / "Zotero" / "storage")
    marker_bin: Path = field(default_factory=lambda: Path.home() / ".local/share/marker/bin/marker_single")
    google_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None

    # Derived paths
    @property
    def papers_dir(self) -> Path:
        return self.refs_dir / "papers"

    @property
    def db_path(self) -> Path:
        return self.refs_dir / "ml4t_refs.db"

    @property
    def papers_index(self) -> Path:
        return self.refs_dir / "papers_index.json"

    @property
    def prompts_dir(self) -> Path:
        return self.refs_dir / "prompts"

    # Known large books to skip parsing
    skip_keys: set = field(default_factory=lambda: {
        'ZXIKS378',  # 621p - Active Portfolio Management
        '433X6B3U',  # 487p - Causality (Pearl)
        'AXBLXSEH',  # 381p - Econometrics of High-Frequency Data
        'D4ID9ERE',  # Causal Inference: What If (large book)
        'VLQ6BNAP',  # Asset Management (large book)
        'VWTB53BW',  # Foundations of RL with Finance (large book)
        'RHDYID8S',  # PhD thesis (likely large)
    })


def load_env_file(env_path: Path) -> dict:
    """Load variables from a .env file."""
    env_vars = {}
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                # Strip quotes
                value = value.strip().strip('"').strip("'")
                env_vars[key.strip()] = value
    return env_vars


def find_project_env() -> Optional[Path]:
    """Find .env file in current directory or parent directories."""
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        env_path = parent / ".env"
        if env_path.exists():
            return env_path
        # Stop at home directory
        if parent == Path.home():
            break
    return None


def get_config() -> Config:
    """
    Load configuration from environment and .env files.

    Priority:
    1. Project .env file
    2. Environment variables
    3. Defaults
    """
    # Start with environment
    env = dict(os.environ)

    # Override with project .env if found
    env_path = find_project_env()
    if env_path:
        env.update(load_env_file(env_path))

    # Required values
    refs_dir = env.get("REFS_DIR")
    if not refs_dir:
        raise ValueError(
            "REFS_DIR not configured. Add to .env file:\n"
            "  REFS_DIR=/path/to/references"
        )

    library_id = env.get("ZOTERO_LIBRARY_ID")
    if not library_id:
        raise ValueError(
            "ZOTERO_LIBRARY_ID not configured. Add to .env file:\n"
            "  ZOTERO_LIBRARY_ID=3  # Your Zotero library ID"
        )

    # Build config
    config = Config(
        refs_dir=Path(refs_dir).expanduser(),
        zotero_library_id=int(library_id),
    )

    # Optional overrides
    if "ZOTERO_DB" in env:
        config.zotero_db = Path(env["ZOTERO_DB"]).expanduser()

    if "ZOTERO_STORAGE" in env:
        config.zotero_storage = Path(env["ZOTERO_STORAGE"]).expanduser()

    if "MARKER_BIN" in env:
        config.marker_bin = Path(env["MARKER_BIN"]).expanduser()

    if "GOOGLE_API_KEY" in env:
        config.google_api_key = env["GOOGLE_API_KEY"]

    if "OPENAI_API_KEY" in env:
        config.openai_api_key = env["OPENAI_API_KEY"]

    return config


def validate_config(config: Config) -> list[str]:
    """Validate configuration and return list of issues."""
    issues = []

    if not config.refs_dir.exists():
        issues.append(f"REFS_DIR does not exist: {config.refs_dir}")

    if not config.zotero_db.exists():
        issues.append(f"Zotero database not found: {config.zotero_db}")

    if not config.marker_bin.exists():
        issues.append(f"Marker binary not found: {config.marker_bin}")

    if not config.google_api_key:
        issues.append("GOOGLE_API_KEY not set (required for summarization)")

    return issues
