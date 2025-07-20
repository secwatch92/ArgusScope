from argus_scope.database.db_manager import DatabaseManager
from argus_scope.core.models import WorkspaceModel, TargetModel, WorkspaceState
from typing import List

class WorkspaceManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def create_workspace(self, name: str, description: str = "") -> WorkspaceModel:
        new_ws = WorkspaceModel(name=name, description=description)
        workspace_id = self.db.create_workspace(new_ws)
        return self.db.get_workspace(workspace_id)

    def add_target(self, workspace_id: str, domain: str, tags: List[str] = []):
        target = TargetModel(domain=domain, tags=tags)
        self.db.add_target(workspace_id, target)
        return self.db.get_workspace(workspace_id)

    def lock_workspace(self, workspace_id: str):
        # جلوگیری از تغییرات حین اسکن
        self.db.update_workspace_state(workspace_id, WorkspaceState.LOCKED)

    def unlock_workspace(self, workspace_id: str):
        self.db.update_workspace_state(workspace_id, WorkspaceState.ACTIVE)