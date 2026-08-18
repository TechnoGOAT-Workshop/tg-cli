from unittest.mock import Mock

from tg.providers.aws_provider import Boto3EnvironmentService


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