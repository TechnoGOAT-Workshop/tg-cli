from dataclasses import dataclass

from tg.domain.resource_action import Action, ResourceAction


@dataclass(frozen=True)
class OperationPlan:
    environment_name: str
    operation: str
    actions: tuple[ResourceAction, ...]

    @property
    def changes(self) -> tuple[ResourceAction, ...]:
        return tuple(
            action
            for action in self.actions
            if action.action is not Action.NONE
        )