from pytest import MonkeyPatch
from typer.testing import CliRunner

from tg.cli import app
from tg.domain.operation_plan import OperationPlan
from tg.domain.resource_action import Action, ResourceAction

runner = CliRunner()


def test_cli_help():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Manage TechnoGOAT development environments." in result.stdout
    assert "env" in result.stdout


def test_env_help():
    result = runner.invoke(app, ["env", "--help"])

    assert result.exit_code == 0


def test_plan_stop_does_not_apply(monkeypatch: MonkeyPatch):
    class FakeService:
        def __init__(self):
            self.apply_called = False

        def plan_stop(self, _environment):
            return OperationPlan(
                environment_name="uts",
                operation="stop",
                actions=(
                    ResourceAction(
                        kind="compute",
                        identifier="uts-moodle-web-01",
                        current_status="running",
                        target_status="stopped",
                        action=Action.STOP,
                    ),
                ),
            )

        def apply(self, _plan):
            self.apply_called = True

    fake_service = FakeService()

    monkeypatch.setattr(
        "tg.commands.env.load_environment",
        lambda name, path: object(),
    )

    monkeypatch.setattr(
        "tg.commands.env.get_environment_service",
        lambda environment: fake_service,
    )

    result = runner.invoke(
        app,
        ["env", "plan", "stop", "uts"],
    )

    assert result.exit_code == 0
    assert not fake_service.apply_called