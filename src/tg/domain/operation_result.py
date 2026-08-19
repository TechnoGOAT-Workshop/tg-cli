from dataclasses import dataclass

from tg.domain.resource_result import ResourceResult


@dataclass(frozen=True)
class OperationResult:
    environment_name: str
    operation: str
    resources: tuple[ResourceResult, ...]

    @property
    def successful(self) -> bool:
        return all(resource.success for resource in self.resources)