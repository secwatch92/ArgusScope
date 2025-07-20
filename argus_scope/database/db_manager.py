# This class is our sole gatekeeper for communicating with the MongoDB fortress.
from pymongo import MongoClient, ASCENDING, ReturnDocument
from typing import Optional, List
from argus_scope.core.models import WorkspaceModel, TargetModel, WorkspaceState, SubdomainModel
from datetime import datetime

class DatabaseManager:
    """Database management class for all CRUD operations."""

    def __init__(self, connection_uri: str):
        self.client = MongoClient(connection_uri)
        self.db = self.client.argus_db  # Name of the database
        self.workspaces = self.db.workspaces
        self.subdomains = self.db.subdomains
        self._create_indexes()

    def _create_indexes(self):
        """To speed up searches, we index the main paths."""
        self.db.workspaces.create_index([("name", ASCENDING)], unique=True)
        self.db.workspaces.create_index([("id", ASCENDING)], unique=True)
        self.db.subdomains.create_index([("workspace_id", ASCENDING)])
        self.db.ports.create_index([("host", ASCENDING)])


    def create_workspace(self, workspace: WorkspaceModel) -> WorkspaceModel:
        """Creates a new Workspace in the database."""
        self.db.workspaces.insert_one(workspace.model_dump())
        print(f"Workspace '{workspace.name}' created successfully in DB.")
        return workspace

    def get_workspace_by_name(self, name: str) -> Optional[WorkspaceModel]:
        """Searches for a Workspace by its unique name."""
        data = self.db.workspaces.find_one({"name": name})
        return WorkspaceModel(**data) if data else None

    def update_workspace_state(self, workspace_name: str, state: WorkspaceState) -> Optional[WorkspaceModel]:
        """Updates the status of a Workspace (e.g., to lock it)."""
        updated_doc = self.db.workspaces.find_one_and_update(
            {"name": workspace_name},
            {"$set": {"state": state.value, "updated_at": datetime.utcnow()}},
            return_document=ReturnDocument.AFTER
        )
        return WorkspaceModel(**updated_doc) if updated_doc else None

    def save_subdomains(self, workspace_id: str, subdomains: List[SubdomainModel]):
        """Stores subdomain scan results in bulk in the database."""
        if not subdomains:
            return
        # Convert Pydantic models to dictionaries for storing in MongoDB
        # We already have workspace_id in the model, so no need to add it again
        subdomain_dicts = [sub.model_dump() for sub in subdomains]
        self.db.subdomains.insert_many(subdomain_dicts)
        print(f"Saved {len(subdomains)} subdomains for workspace with ID '{workspace_id}'.")

    def update_scan_stats(self, workspace_name: str, stats: dict):
        """Saves the latest scan statistics in the Workspace document."""
        self.db.workspaces.update_one(
            {"name": workspace_name},
            {"$set": {"scan_stats": stats, "updated_at": datetime.utcnow()}}
        )

    def add_target_to_workspace(self, workspace_name: str, target: TargetModel) -> Optional[WorkspaceModel]: # <--- اصلاحیه: نام متد اصلاح شد
        """Adds a new target to a Workspace's target list."""
        updated_doc = self.db.workspaces.find_one_and_update(
            {"name": workspace_name},
            {"$push": {"targets": target.model_dump()}},
            return_document=ReturnDocument.AFTER
        )
        return WorkspaceModel(**updated_doc) if updated_doc else None

    def get_subdomains_by_workspace_name(self, workspace_name: str) -> List[SubdomainModel]:
        """Retrieves all subdomains related to a Workspace."""
        workspace = self.get_workspace_by_name(workspace_name)
        if not workspace:
            return []

        subdomain_data = self.db.subdomains.find({"workspace_id": workspace.id})
        return [SubdomainModel(**data) for data in subdomain_data]