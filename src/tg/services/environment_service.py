from abc import ABC, abstractmethod

from tg.domain.environment import Environment
from tg.domain.status import EnvironmentStatus

class EnvironmentService(ABC):

    @abstractmethod
    def status(self, environment: Environment) -> EnvironmentStatus:
        pass

    @abstractmethod
    def start(self, environment: Environment) -> None:
        pass

    @abstractmethod
    def stop(self, environment: Environment) -> None:
        pass