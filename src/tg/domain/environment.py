from dataclasses import dataclass

from tg.domain.resource import Resource


@dataclass(slots=True, frozen=True)
class Environment:
    name: str
    provider: str
    profile: str
    region: str
    resources: tuple[Resource, ...] = ()