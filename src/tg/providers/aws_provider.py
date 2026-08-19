import boto3

from tg.domain.environment import Environment
from tg.domain.operation_plan import OperationPlan
from tg.domain.operation_result import OperationResult
from tg.domain.resource import ResourceType
from tg.domain.resource_action import Action, ResourceAction
from tg.domain.resource_result import ResourceResult
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

    from tg.domain.status import EnvironmentStatus

    def status(self, environment: Environment) -> EnvironmentStatus:
        states = []

        for resource in environment.resources:
            if resource.type == ResourceType.COMPUTE:
                states.append(self._get_ec2_status(resource.name))

        if not states:
            return EnvironmentStatus.UNKNOWN

        if all(state == "running" for state in states):
            return EnvironmentStatus.RUNNING

        if all(state == "stopped" for state in states):
            return EnvironmentStatus.STOPPED

        return EnvironmentStatus.PARTIAL

    def start(self, environment: Environment) -> None:
        pass

    def plan_stop(self, environment: Environment) -> OperationPlan:
        actions = []

        for resource in environment.resources:
            if resource.type == ResourceType.COMPUTE:
                current_status = self._get_ec2_status(resource.name)

                if current_status == "running":
                    actions.append(
                        ResourceAction(
                            kind=resource.type.value,
                            identifier=resource.name,
                            current_status=current_status,
                            target_status="stopped",
                            action=Action.STOP,
                        )
                    )

                elif current_status == "stopped":
                    actions.append(
                        ResourceAction(
                            kind=resource.type.value,
                            identifier=resource.name,
                            current_status=current_status,
                            target_status="stopped",
                            action=Action.NONE,
                            reason="Already stopped",
                        )
                    )

        return OperationPlan(
            environment_name=environment.name,
            operation="stop",
            actions=tuple(actions),
        )

    def apply(
            self,
            plan: OperationPlan,
    ) -> OperationResult:
        results = []

        for resource_action in plan.actions:
            if resource_action.action is Action.NONE:
                results.append(
                    ResourceResult(
                        kind=resource_action.kind,
                        identifier=resource_action.identifier,
                        previous_status=resource_action.current_status,
                        current_status=resource_action.current_status,
                        success=True,
                        message=resource_action.reason,
                    )
                )
                continue

            if resource_action.action is Action.STOP:
                self._stop_ec2_instance(
                    resource_action.identifier
                )

                current_status = self._get_ec2_status(
                    resource_action.identifier
                )

                success = (
                        current_status
                        == resource_action.target_status
                )

                results.append(
                    ResourceResult(
                        kind=resource_action.kind,
                        identifier=resource_action.identifier,
                        previous_status=resource_action.current_status,
                        current_status=current_status,
                        success=success,
                        message=None if success else (
                            "Resource did not reach target state"
                        ),
                    )
                )

        return OperationResult(
            environment_name=plan.environment_name,
            operation=plan.operation,
            resources=tuple(results),
        )

    def _get_ec2_status(self, name: str) -> str:
        response = self._ec2.describe_instances(
            Filters=[
                {
                    "Name": "tag:Name",
                    "Values": [name],
                }
            ]
        )

        reservations = response["Reservations"]

        if not reservations:
            return "unknown"

        instance = reservations[0]["Instances"][0]

        return instance["State"]["Name"]

    def _find_instance_id(self, name: str) -> str:
        response = self._ec2.describe_instances(
            Filters=[
                {
                    "Name": "tag:Name",
                    "Values": [name],
                }
            ]
        )

        reservations = response.get("Reservations", [])

        if not reservations:
            raise ValueError(
                f"No compute resource found with name {name}"
            )

        return reservations[0]["Instances"][0]["InstanceId"]

    def _stop_ec2_instance(
            self,
            name: str,
    ) -> None:
        instance_id = self._find_instance_id(name)

        self._ec2.stop_instances(
            InstanceIds=[instance_id]
        )

        waiter = self._ec2.get_waiter(
            "instance_stopped"
        )

        waiter.wait(
            InstanceIds=[instance_id]
        )
