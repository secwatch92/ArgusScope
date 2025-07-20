import typer
from argus_scope.core.engine import ScanEngine
from argus_scope.core.models import WorkspaceModel, TargetModel
from argus_scope.utils.db import get_db_manager
import asyncio


app = typer.Typer(help="ArgusScope - A Comprehensive Reconnaissance Platform")
workspace_app = typer.Typer(help="Manage reconnaissance workspaces.")
app.add_typer(workspace_app, name="workspace")


# --- CLI commands ---
@workspace_app.command("create")
def create_workspace_cli(
        name: str = typer.Option(..., "--name", "-n", help="A unique name for the new workspace."),
        description: str = typer.Option(None, "--description", "-d", help="A brief description for the workspace.")
):
    """    Creates a new Workspace for a reconnaissance target.    """
    db = get_db_manager()
    typer.echo(f"Attempting to create workspace '{name}'...")

    if db.get_workspace_by_name(name):
        typer.secho(f"Error: A workspace with the name '{name}' already exists.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    new_workspace = WorkspaceModel(name=name, description=description)
    created_ws = db.create_workspace(new_workspace)

    typer.secho(f"✅ Workspace '{created_ws.name}' created successfully!", fg=typer.colors.GREEN)
    typer.echo(f"   ID: {created_ws.id}")
    typer.echo(f"   Description: {created_ws.description or 'N/A'}")


@workspace_app.command("add-target")
def add_target_cli(
        workspace_name: str = typer.Option(..., "--workspace", "-w", help="Name of the workspace."),
        domain: str = typer.Option(..., "--domain", "-D", help="The domain to add as a target."),
        tags: str = typer.Option(None, "--tags", "-t", help="Comma-separated tags (e.g., 'web,prod').")
):
    """Adds a new target to an existing Workspace."""
    db = get_db_manager()
    if not db.get_workspace_by_name(workspace_name):
        typer.secho(f"Error: Workspace '{workspace_name}' not found.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    tag_list = [t.strip() for t in tags.split(",")] if tags else []
    target = TargetModel(domain=domain, tags=tag_list)

    db.add_target_to_workspace(workspace_name, target)
    typer.secho(f"✅ Target '{domain}' added to workspace '{workspace_name}' successfully!", fg=typer.colors.GREEN)

@workspace_app.command("list-subdomains")
def list_subdomains_cli(
        workspace_name: str = typer.Option(..., "--workspace", "-w",
                                           help="Name of the workspace to list subdomains for.")
):
    """ Displays the list of all discovered subdomains for a Workspace."""
    db = get_db_manager()
    typer.echo(f"Fetching subdomains for workspace '{workspace_name}'...")

    subdomains = db.get_subdomains_by_workspace_name(workspace_name)

    if not subdomains:
        typer.secho(f"No subdomains found for workspace '{workspace_name}'. Run a scan first.", fg=typer.colors.YELLOW)
        return

    typer.secho(f"✅ Found {len(subdomains)} subdomains:", fg=typer.colors.GREEN)
    for sub in subdomains:
        ips = ", ".join(sub.ip_addresses) if sub.ip_addresses else "N/A"
        typer.echo(f"  - {sub.name} (IPs: {ips}, Source: {sub.source})")

@app.command("scan")
def run_scan_cli(
        workspace_name: str = typer.Option(..., "--workspace", "-w", help="Name of the workspace to scan.")
):
    """Performs a full scan on the specified Workspace."""
    db = get_db_manager()
    engine = ScanEngine(db_manager=db)

    typer.echo(f"🚀 Starting a full scan on workspace '{workspace_name}'...")

    # Run the async function using asyncio.run.
    scan_results = asyncio.run(engine.run_scan(workspace_name))

    typer.secho("✨ Scan complete!", fg=typer.colors.BRIGHT_GREEN)
    typer.echo("--- Scan Statistics ---")
    for key, value in scan_results.items():
        typer.echo(f"   {key.replace('_', ' ').title()}: {value}")
if __name__ == "__main__":
    app()