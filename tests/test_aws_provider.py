from unittest.mock import Mock
from pathlib import Path

from tg.config.loader import load_environment
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

def test_stop_stops_compute_instance():
    session = Mock()

    ec2 = Mock()
    ec2.describe_instances.return_value = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-12345"
                    }
                ]
            }
        ]
    }

    session.client.side_effect = lambda name: {
        "ec2": ec2,
        "rds": Mock(),
    }.get(name)

    service = Boto3EnvironmentService(session)

    environment = load_environment(
        "uts",
        Path("examples/tg.yaml")
    )
    service.stop(environment)

    ec2.stop_instances.assert_called_with(
        InstanceIds=["i-12345"]
    )