from enum import Enum


class EnvironmentStatus(str, Enum):
    """High-level engineering status."""

    RUNNING = "running"
    STOPPED = "stopped"
    PARTIAL = "partial"
    UNKNOWN = "unknown"
