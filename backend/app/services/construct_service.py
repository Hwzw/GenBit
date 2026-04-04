"""Construct CRUD operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.construct import Construct
from app.models.construct_element import ConstructElement
from app.schemas.construct import ConstructCreate, ConstructUpdate


async def get_construct(db: AsyncSession, construct_id: uuid.UUID) -> Construct | None:
    result = await db.execute(
        select(Construct)
        .options(selectinload(Construct.elements))
        .where(Construct.id == construct_id)
    )
    return result.scalar_one_or_none()


async def create_construct(db: AsyncSession, data: ConstructCreate) -> Construct:
    construct = Construct(
        project_id=data.project_id,
        name=data.name,
        organism_tax_id=data.organism_tax_id,
    )
    db.add(construct)
    await db.flush()

    for elem in data.elements:
        db.add(ConstructElement(
            construct_id=construct.id,
            element_type=elem.element_type,
            label=elem.label,
            sequence=elem.sequence,
            position=elem.position,
            metadata_json=elem.metadata_json,
        ))

    await db.commit()
    await db.refresh(construct)
    return construct


async def update_construct(
    db: AsyncSession, construct_id: uuid.UUID, data: ConstructUpdate
) -> Construct | None:
    construct = await get_construct(db, construct_id)
    if not construct:
        return None
    if data.name is not None:
        construct.name = data.name
    if data.organism_tax_id is not None:
        construct.organism_tax_id = data.organism_tax_id
    await db.commit()
    await db.refresh(construct)
    return construct


async def delete_construct(db: AsyncSession, construct_id: uuid.UUID) -> bool:
    construct = await db.get(Construct, construct_id)
    if not construct:
        return False
    await db.delete(construct)
    await db.commit()
    return True
