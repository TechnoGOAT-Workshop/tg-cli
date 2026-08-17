from pathlib import Path

from tg.config.loader import load_environment
from tg.domain.resource import ResourceType


def test_load_environment(tmp_path: Path):
    config_path = tmp_path / "tg.yaml"

    config_path.write_text(
        """
environments:
  uts:
    provider: aws
    profile: uts-validation
    region: us-east-1

    resources:
      - name: uts-moodle-web-01
        type: compute
"""
    )

    environment = load_environment("uts", config_path)

    assert environment.name == "uts"
    assert environment.provider == "aws"
    assert environment.profile == "uts-validation"
    assert environment.region == "us-east-1"

    assert len(environment.resources) == 1

    resource = environment.resources[0]

    assert resource.name == "uts-moodle-web-01"
    assert resource.type is ResourceType.COMPUTE
