from rich.console import Console
from rich.table import Table

from tg.domain.operation_plan import OperationPlan


def render_operation_plan(
    plan: OperationPlan,
    console: Console | None = None,
) -> None:
    console = console or Console()

    console.print(
        f"[bold]Environment:[/bold] {plan.environment_name}"
    )
    console.print(
        f"[bold]Operation:[/bold] {plan.operation}"
    )

    table = Table(
        "Resource",
        "Current",
        "Target",
        "Action",
        "Reason",
    )

    for action in plan.actions:
        table.add_row(
            action.identifier,
            str(action.current_status),
            str(action.target_status),
            action.action.value,
            action.reason or "",
        )

    console.print(table)