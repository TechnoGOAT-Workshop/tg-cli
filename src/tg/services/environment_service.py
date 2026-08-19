from abc import ABC, abstractmethod

from tg.domain.environment import Environment
from tg.domain.operation_plan import OperationPlan
from tg.domain.operation_result import OperationResult
from tg.domain.status import EnvironmentStatus


class EnvironmentService(ABC):

    @abstractmethod
    def status(self, environment: Environment) -> EnvironmentStatus:
        pass

    @abstractmethod
    def start(self, environment: Environment) -> None:
        pass

    @abstractmethod
    def plan_stop(self, environment: Environment) -> OperationPlan:
        pass

    @abstractmethod
    def apply(self, plan: OperationPlan) -> OperationResult:
        pass
