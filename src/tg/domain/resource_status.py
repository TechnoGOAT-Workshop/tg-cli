from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceStatus:
    kind: str
    identifier: str
    status: str