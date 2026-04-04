import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.schemas.construct import ConstructCreate, ConstructResponse, ConstructUpdate
from app.services import construct_assembly_service, construct_service

router = APIRouter()


@router.post("/", response_model=ConstructResponse)
async def create_construct(data: ConstructCreate, db: AsyncSession = Depends(get_db)):
    return await construct_service.create_construct(db, data)


@router.get("/{construct_id}", response_model=ConstructResponse)
async def get_construct(construct_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    construct = await construct_service.get_construct(db, construct_id)
    if not construct:
        raise HTTPException(status_code=404, detail="Construct not found")
    return construct


@router.put("/{construct_id}", response_model=ConstructResponse)
async def update_construct(
    construct_id: uuid.UUID, data: ConstructUpdate, db: AsyncSession = Depends(get_db)
):
    construct = await construct_service.update_construct(db, construct_id, data)
    if not construct:
        raise HTTPException(status_code=404, detail="Construct not found")
    return construct


@router.delete("/{construct_id}")
async def delete_construct(construct_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    deleted = await construct_service.delete_construct(db, construct_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Construct not found")
    return {"status": "deleted"}


@router.post("/{construct_id}/assemble")
async def assemble_construct(construct_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    construct = await construct_service.get_construct(db, construct_id)
    if not construct:
        raise HTTPException(status_code=404, detail="Construct not found")
    elements = [
        ConstructCreate.model_validate(e, from_attributes=True) for e in construct.elements
    ]
    return construct_assembly_service.assemble_construct(elements)
