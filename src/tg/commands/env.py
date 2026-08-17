import typer

env_app = typer.Typer(help="Manage engineering environments.")


@env_app.command("status")
def status(name: str):
    typer.echo(f"Environment: {name}")