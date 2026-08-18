import typer

from tg.config.loader import load_environment
from tg.services.provider_factory import get_environment_service

env_app = typer.Typer(help="Manage engineering environments.")


@env_app.command("status")
def status(ctx: typer.Context, name: str):
    environment = load_environment(
        name,
        ctx.obj["config_path"],
    )

    service = get_environment_service(environment)

    result = service.status(environment)

    typer.echo(
        f"{name}: {result.value}"
    )

@env_app.command("stop")
def stop(ctx: typer.Context, name: str):
    environment = load_environment(
        name,
        ctx.obj["config_path"],
    )

    service = get_environment_service(environment)

    stopped = service.stop(environment)

    for resource in stopped:
        print(f"Stopped: {resource}")
