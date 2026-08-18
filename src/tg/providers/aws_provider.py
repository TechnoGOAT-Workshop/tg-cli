import boto3

from tg.domain.environment import Environment
from tg.domain.status import EnvironmentStatus
from tg.services.environment_service import EnvironmentService


class Boto3EnvironmentService(EnvironmentService):
    """AWS implementation of environment management."""

    def __init__(self, session: boto3.Session) -> None:
        self._session = session
        self._ec2 = session.client("ec2")
        self._rds = session.client("rds")

    @classmethod
    def from_environment(
        cls,
        environment: Environment,
    ) -> "Boto3EnvironmentService":
        session = boto3.Session(
            profile_name=environment.profile,
            region_name=environment.region,
        )
        return cls(session)

    def identity(self) -> dict:
        return self._session.client("sts").get_caller_identity()

    def status(self, environment: Environment) -> EnvironmentStatus:
        return EnvironmentStatus.UNKNOWN

    def start(self, environment: Environment) -> None:
        pass

    def stop(self, environment: Environment) -> None:
        pass