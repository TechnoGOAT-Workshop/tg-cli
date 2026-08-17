from dataclasses import dataclass
from enum import Enum


class ResourceType(str, Enum):
    COMPUTE = "compute"
    DATABASE = "database"


@dataclass(slots=True, frozen=True)
class Resource:
    name: str
    type: ResourceType