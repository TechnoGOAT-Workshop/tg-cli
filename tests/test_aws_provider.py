from unittest.mock import Mock

from tg.domain.operation_plan import OperationPlan
from tg.domain.resource_action import Action, ResourceAction
from tg.providers.aws_provider import Boto3EnvironmentService
from tg.services.environment_service import EnvironmentService


def test_identity_uses_sts():
    session = Mock()

    sts = Mock()
    sts.get_caller_identity.return_value = {
        "Account": "147997115266",
        "Arn": "test-arn",
    }

    session.client.return_value = sts

    service = Boto3EnvironmentService(session)

    identity = service.identity()

    assert identity["Account"] == "147997115266"
    session.client.assert_called_with("sts")


def test_aws_service_implements_environment_service():
    session = Mock()

    service = Boto3EnvironmentService(session)

    assert isinstance(service, EnvironmentService)


def test_apply_stops_compute_instance(aws_service):
    service, ec2 = aws_service

    ec2.describe_instances.return_value = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-12345",
                        "State": {
                            "Name": "stopped"
                        },
                    }
                ]
            }
        ]
    }

    plan = OperationPlan(
        environment_name="uts",
        operation="stop",
        actions=(
            ResourceAction(
                kind="compute",
                identifier="uts-moodle-web-01",
                current_status="running",
                target_status="stopped",
                action=Action.STOP,
            ),
        ),
    )

    service.apply(plan)

    ec2.stop_instances.assert_called_once_with(
        InstanceIds=["i-12345"]
    )


def test_apply_does_not_execute_no_action(aws_service):
    service, ec2 = aws_service

    plan = OperationPlan(
        environment_name="uts",
        operation="stop",
        actions=(
            ResourceAction(
                kind="compute",
                identifier="uts-moodle-web-01",
                current_status="stopped",
                target_status="stopped",
                action=Action.NONE,
                reason="Already stopped",
            ),
        ),
    )

    service.apply(plan)

    ec2.stop_instances.assert_not_called()
