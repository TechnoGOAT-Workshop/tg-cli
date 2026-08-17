from pathlib import Path

import yaml

from tg.domain.environment import Environment
from tg.domain.resource import Resource, ResourceType


def load_environment(name: str, config_path: Path) -> Environment:
    with config_path.open() as config_file:
        config = yaml.safe_load(config_file)

    environments = config.get("environments", {})

    if name not in environments:
        raise ValueError(f"Environment '{name}' was not found.")

    environment_config = environments[name]

    resources = tuple(
        Resource(
            name=resource["name"],
            type=ResourceType(resource["type"]),
        )
        for resource in environment_config.get("resources", [])
    )

    return Environment(
        name=name,
        provider=environment_config["provider"],
        profile=environment_config["profile"],
        region=environment_config["region"],
        resources=resources,
    )