from fastapi import APIRouter, HTTPException
from argus_scope.core.engine import run_scan
from argus_scope.utils.exceptions import InvalidTargetError

router = APIRouter()

@router.post("/scan")
async def start_scan(target: str):
    try:
        results = run_scan(target)
        return {"status": "success", "results": results}
    except InvalidTargetError as e:
        raise HTTPException(status_code=400, detail=str(e))
