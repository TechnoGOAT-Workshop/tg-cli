import typer

from tg.config.loader import load_environment
from tg.presentation.operation_plan_renderer import render_operation_plan
from tg.presentation.operation_result_renderer import render_operation_result
from tg.services.provider_factory import get_environment_service

env_app = typer.Typer(help="Manage engineering environments.")
plan_app = typer.Typer(
    help="Preview environment operations without applying changes."
)

env_app.add_typer(plan_app, name="plan")


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

    plan = service.plan_stop(environment)

    render_operation_plan(plan)

    if not plan.changes:
        typer.echo("No changes required.")
        return

    if not typer.confirm("Apply this plan?"):
        typer.echo("Operation cancelled.")
        return

    typer.echo("Applying plan and waiting for resources to reach their target state...")

    result = service.apply(plan)

    render_operation_result(result)


@plan_app.command("stop")
def plan_stop(ctx: typer.Context, name: str):
    environment = load_environment(
        name,
        ctx.obj["config_path"],
    )

    service = get_environment_service(environment)

    plan = service.plan_stop(environment)

    render_operation_plan(plan)

    if not plan.changes:
        typer.echo("No changes required.")
