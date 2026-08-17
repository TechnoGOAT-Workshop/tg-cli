from typer.testing import CliRunner

from tg.cli import app

runner = CliRunner()


def test_cli_help():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Manage TechnoGOAT development environments." in result.stdout
    assert "env" in result.stdout

def test_env_help():
    result = runner.invoke(app, ["env", "--help"])

    assert result.exit_code == 0