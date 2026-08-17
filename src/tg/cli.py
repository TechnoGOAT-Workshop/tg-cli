from pathlib import Path
from typing import Annotated

import typer

from tg.commands.env import env_app

app = typer.Typer(help="Manage TechnoGOAT development environments.", no_args_is_help=True)
app.add_typer(env_app, name="env")


@app.callback()
def main(
    ctx: typer.Context,
    config: Annotated[
        Path,
        typer.Option("--config", "-c", help="Path to the TG CLI YAML configuration."),
    ] = Path("tg.yaml"),
) -> None:
    """Manage TechnoGOAT development environments."""
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config


if __name__ == "__main__":
    app()
