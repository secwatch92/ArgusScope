import uuid
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum

class WorkspaceState(str, Enum):
    """وضعیت‌های مختلف یک Workspace را تعریف می‌کند."""
    ACTIVE = "active"
    ARCHIVED = "archived"
    LOCKED = "locked"  # برای زمانی که یک اسکن در حال اجراست

class TargetModel(BaseModel):
    """مدل داده برای یک هدف مشخص در داخل Workspace."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    domain: str
    ip_range: Optional[str] = None
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class WorkspaceModel(BaseModel):
    """مدل داده اصلی برای یک Workspace."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    state: WorkspaceState = WorkspaceState.ACTIVE
    targets: List[TargetModel] = []
    metadata: Dict = {}
    scan_stats: Dict = Field(default_factory=dict)
class SubdomainModel(BaseModel):
    """مدل داده برای یک زیردامنه کشف‌شده."""
    workspace_id: str
    name: str
    ip_addresses: List[str] = []
    source: str  # منبع کشف (مثلاً: subfinder, crt.sh)
    discovered_at: datetime = Field(default_factory=datetime.utcnow)
    last_seen: datetime = Field(default_factory=datetime.utcnow)

class PortModel(BaseModel):
    """مدل داده برای یک پورت باز."""
    workspace_id: str
    host: str # می‌تواند IP یا زیردامنه باشد
    port: int
    protocol: str  # tcp/udp
    service: Optional[str] = None
    banner: Optional[str] = None
    discovered_at: datetime = Field(default_factory=datetime.utcnow)

class WorkspaceModel(BaseModel):
    """مدل داده اصلی برای یک Workspace."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    state: WorkspaceState = WorkspaceState.ACTIVE
    targets: List[TargetModel] = []
    metadata: Dict = {}
    scan_stats: Dict = Field(default_factory=dict)
