from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceResult:
    kind: str
    identifier: str
    previous_status: str
    current_status: str
    success: bool
    message: str | None = None