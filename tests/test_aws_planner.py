from pathlib import Path

from tg.config.loader import load_environment
from tg.domain.resource_action import Action


def test_plan_stop_running_compute_creates_stop_action(
    aws_service,
):
    service, ec2 = aws_service

    ec2.describe_instances.return_value = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-12345",
                        "State": {
                            "Name": "running"
                        },
                    }
                ]
            }
        ]
    }

    environment = load_environment(
        "uts",
        Path("examples/tg.yaml"),
    )

    plan = service.plan_stop(environment)

    assert len(plan.actions) == 1

    action = plan.actions[0]

    assert action.identifier == "uts-moodle-web-01"
    assert action.action is Action.STOP
    assert action.current_status == "running"
    assert action.target_status == "stopped"


def test_plan_stop_stopped_compute_creates_no_action(
    aws_service,
):
    service, ec2 = aws_service

    ec2.describe_instances.return_value = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-12345",
                        "State": {
                            "Name": "stopped"
                        },
                    }
                ]
            }
        ]
    }

    environment = load_environment(
        "uts",
        Path("examples/tg.yaml"),
    )

    plan = service.plan_stop(environment)

    assert len(plan.actions) == 1

    action = plan.actions[0]

    assert action.identifier == "uts-moodle-web-01"
    assert action.action is Action.NONE
    assert action.current_status == "stopped"
    assert action.target_status == "stopped"
    assert action.reason == "Already stopped"