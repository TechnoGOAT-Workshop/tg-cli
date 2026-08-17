# Architecture

The CLI has three small layers:

1. `cli.py` and `commands/env.py` translate terminal input into application calls.
2. `services/config.py` loads and validates local YAML configuration.
3. `services/aws.py` owns all boto3 interaction.

Commands depend on the `EnvironmentService` protocol, not directly on boto3.
This makes the CLI easy to test and leaves one place to add role assumption,
account aliases, alternate credential providers, or richer AWS behavior later.

The configuration selects a region and optional AWS profile per environment.
`Boto3EnvironmentService` creates clients from that environment's session.
No credentials are stored by TG CLI.

