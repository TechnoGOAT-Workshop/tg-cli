from rich.console import Console
from rich.table import Table

from tg.domain.operation_result import OperationResult


def render_operation_result(
    result: OperationResult,
    console: Console | None = None,
) -> None:
    console = console or Console()

    console.print()
    console.print(
        f"[bold]Operation complete:[/bold] {result.operation}"
    )

    table = Table(
        "Resource",
        "Before",
        "After",
        "Result",
        "Message",
    )

    for resource in result.resources:
        table.add_row(
            resource.identifier,
            str(resource.previous_status),
            str(resource.current_status),
            "success" if resource.success else "failed",
            resource.message or "",
        )

    console.print(table)