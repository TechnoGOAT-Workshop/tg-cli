from tg.domain.resource import Resource, ResourceType
from tg.domain.status import EnvironmentStatus
from tg.providers.aws_provider import Boto3EnvironmentService

from tg.domain.environment import Environment
from tg.services.environment_service import EnvironmentService


def get_environment_service(environment: Environment) -> EnvironmentService:
    if environment.provider == "aws":
        return Boto3EnvironmentService.from_environment(environment)

    raise ValueError(
        f"Unsupported provider: {environment.provider}"
    )


def test_status_returns_running_for_running_instance():
    session = Mock()

    ec2 = Mock()
    ec2.describe_instances.return_value = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "State": {"Name": "running"}
                    }
                ]
            }
        ]
    }

    session.client.side_effect = lambda name: ec2

    service = Boto3EnvironmentService(session)

    environment = Environment(
        name="uts",
        provider="aws",
        profile="uts-admin",
        region="us-east-1",
        resources=(
            Resource(
                name="uts-moodle-web-01",
                type=ResourceType.COMPUTE,
            ),
        ),
    )

    assert service.status(environment) == EnvironmentStatus.RUNNING