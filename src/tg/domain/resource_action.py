from dataclasses import dataclass
from enum import StrEnum


class Action(StrEnum):
    STOP = "stop"
    NONE = "none"


@dataclass(frozen=True)
class ResourceAction:
    kind: str
    identifier: str
    current_status: str
    target_status: str
    action: Action
    reason: str | None = None