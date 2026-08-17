from dataclasses import dataclass
from typing import Protocol

import boto3

from tg.config.loader import EnvironmentConfig


@dataclass(frozen=True)
class ResourceStatus:
    kind: str
    identifier: str
    status: str


class EnvironmentService(Protocol):
    def status(self, environment: EnvironmentConfig) -> list[ResourceStatus]: ...

    def start(self, environment: EnvironmentConfig) -> None: ...

    def stop(self, environment: EnvironmentConfig) -> None: ...


class Boto3EnvironmentService:
    """The only layer that knows how AWS credentials and boto3 clients work."""

    def __init__(self, session: boto3.Session) -> None:
        self._ec2 = session.client("ec2")
        self._rds = session.client("rds")

    @classmethod
    def from_config(cls, environment: EnvironmentConfig) -> "Boto3EnvironmentService":
        session = boto3.Session(
            profile_name=environment.profile,
            region_name=environment.region,
        )
        return cls(session)

    def status(self, environment: EnvironmentConfig) -> list[ResourceStatus]:
        statuses: list[ResourceStatus] = []
        if environment.ec2:
            response = self._ec2.describe_instances(InstanceIds=list(environment.ec2))
            instances = (
                instance
                for reservation in response["Reservations"]
                for instance in reservation["Instances"]
            )
            statuses.extend(
                ResourceStatus("ec2", item["InstanceId"], item["State"]["Name"])
                for item in instances
            )
        for identifier in environment.rds:
            response = self._rds.describe_db_instances(DBInstanceIdentifier=identifier)
            database = response["DBInstances"][0]
            statuses.append(
                ResourceStatus("rds", identifier, database["DBInstanceStatus"])
            )
        return statuses

    def start(self, environment: EnvironmentConfig) -> None:
        if environment.ec2:
            self._ec2.start_instances(InstanceIds=list(environment.ec2))
            self._ec2.get_waiter("instance_running").wait(InstanceIds=list(environment.ec2))
        for identifier in environment.rds:
            self._rds.start_db_instance(DBInstanceIdentifier=identifier)
            self._rds.get_waiter("db_instance_available").wait(
                DBInstanceIdentifier=identifier
            )

    def stop(self, environment: EnvironmentConfig) -> None:
        if environment.ec2:
            self._ec2.stop_instances(InstanceIds=list(environment.ec2))
            self._ec2.get_waiter("instance_stopped").wait(InstanceIds=list(environment.ec2))
        for identifier in environment.rds:
            self._rds.stop_db_instance(DBInstanceIdentifier=identifier)
            self._rds.get_waiter("db_instance_stopped").wait(
                DBInstanceIdentifier=identifier
            )

