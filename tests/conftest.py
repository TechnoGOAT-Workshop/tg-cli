# tests/conftest.py

from unittest.mock import Mock

import pytest

from tg.providers.aws_provider import Boto3EnvironmentService


@pytest.fixture
def aws_service():
    session = Mock()
    ec2 = Mock()
    rds = Mock()

    session.client.side_effect = lambda name: {
        "ec2": ec2,
        "rds": rds,
    }.get(name)

    service = Boto3EnvironmentService(session)

    return service, ec2