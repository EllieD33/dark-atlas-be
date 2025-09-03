from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional

from app.db import get_session
from app.schemas.ioc import IOCResponse
from app.services.ioc_service import list_iocs, list_iocs_in_range

router = APIRouter()


@router.get("/", tags=["root"])
async def root():
    return {
        "service": "DarkAtlas Threat API",
        "version": "0.1.0",
        "docs_url": "/docs"
    }


@router.get("/iocs", response_model=list[IOCResponse])
async def list_iocs(session: AsyncSession = Depends(get_session), page: int = 1, limit: int = 1):
    return await list_iocs(session, page, limit)


@router.get("/iocs/range", response_model=list[IOCResponse])
async def list_iocs_in_range(session: AsyncSession = Depends(get_session),
                             start_date: Optional[datetime] = Query(None),
                             end_date: Optional[datetime] = Query(None),
                             page: int = 1,
                             limit: int = 100):
    return await list_iocs_in_range(session, start_date, end_date, page, limit)
