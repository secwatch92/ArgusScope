# این فایل، نقشه راه API ما برای تمام عملیات مربوط به Workspace است.

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from argus_scope.core.models import WorkspaceModel
from argus_scope.database.db_manager import DatabaseManager
from argus_scope.utils.db import get_db_manager

# یک روتر جدید برای گروه‌بندی تمام endpointهای مربوط به workspace می‌سازیم.
router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"],
)


@router.post("/", response_model=WorkspaceModel, status_code=status.HTTP_201_CREATED)
def create_workspace(
        name: str,
        description: Optional[str] = None,
        db: DatabaseManager = Depends(get_db_manager)
):
    """
    یک Workspace جدید برای یک هدف شناسایی ایجاد می‌کند.
    """
    if db.get_workspace_by_name(name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Workspace with name '{name}' already exists."
        )

    new_workspace = WorkspaceModel(name=name, description=description)
    created_ws = db.create_workspace(new_workspace)
    return created_ws
