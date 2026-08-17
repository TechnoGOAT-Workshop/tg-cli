from tg.domain.environment import Environment


def test_environment_creation():
    environment = Environment(
        name="uts",
        provider="aws",
        profile="default",
        region="us-east-1",
    )

    assert environment.name == "uts"
    assert environment.provider == "aws"
    assert environment.profile == "default"
    assert environment.region == "us-east-1"