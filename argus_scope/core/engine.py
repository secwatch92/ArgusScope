import asyncio
import subprocess  # nosec B404
from datetime import datetime
from typing import List

from argus_scope.database.db_manager import DatabaseManager
from argus_scope.core.models import WorkspaceModel, TargetModel, SubdomainModel, WorkspaceState


class ScanEngine:
    """
    The main engine for coordinating and executing scanning modules.
    This class is completely independent from the CLI and API.
    """

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    async def _run_subfinder(self, domain: str) -> List[str]:
        """Runs the subfinder tool asynchronously and returns its output."""

        command = ["subfinder", "-d", domain, "-silent"]
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            print(f"Error running subfinder for {domain}: {stderr.decode()}")
            return []

        # Clean the output and return it as a list
        return stdout.decode().strip().split('\n')

    async def run_scan(self, workspace_name: str) -> dict:
        # Performs a full scan on all targets of a specified Workspace.

        print(f"Engine starting scan for workspace: {workspace_name}")
        workspace = self.db.get_workspace_by_name(workspace_name)
        if not workspace:
            raise ValueError(f"Workspace '{workspace_name}' not found.")

        self.db.update_workspace_state(workspace_name, WorkspaceState.LOCKED)

        scan_start_time = datetime.utcnow()
        all_discovered_subdomains = []

        try:
            for target in workspace.targets:
                print(f"  -> Scanning target: {target.domain}")

                print(f"     -> Running Subdomain Enumeration for {target.domain}...")
                subfinder_results = await self._run_subfinder(target.domain)

                # Convert the textual output to Pydantic data models
                discovered_subs = [
                    SubdomainModel(workspace_id=workspace.id, name=sub.strip(), source="subfinder")
                    for sub in subfinder_results if sub.strip()
                ]
                all_discovered_subdomains.extend(discovered_subs)
                print(f"     <- Found {len(discovered_subs)} new subdomains.")

            # Store all results in the database
            self.db.save_subdomains(workspace.id, all_discovered_subdomains)

        finally:
            print(f"Engine finishing scan for workspace: {workspace_name}")
            self.db.update_workspace_state(workspace_name, WorkspaceState.ACTIVE)

        # Update scan statistics
        scan_end_time = datetime.utcnow()
        stats = {
            "start_time": scan_start_time.isoformat(),
            "end_time": scan_end_time.isoformat(),
            "duration_seconds": (scan_end_time - scan_start_time).total_seconds(),
            "targets_scanned": len(workspace.targets),
            "subdomains_found": len(all_discovered_subdomains)
        }
        self.db.update_scan_stats(workspace_name, stats)

        return stats