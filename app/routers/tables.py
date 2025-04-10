from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.models import Reservation
from app.models.table import Table
from app.schemas.table import TableCreate
from typing import List
import logging


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=List[Table])
def get_tables(session: Session = Depends(get_session)):
    logger.info("Fetching all tables.")
    tables = session.exec(select(Table)).all()
    logger.info(f"Found {len(tables)} tables.")
    return tables


@router.post("/", response_model=Table)
def create_table(table: TableCreate, session: Session = Depends(get_session)):
    logger.info(f"Creating table: {table.name}, Seats: {table.seats}, Location: {table.location}")
    db_table = Table(**table.model_dump())
    session.add(db_table)
    session.commit()
    session.refresh(db_table)
    logger.info(f"Table created with ID: {db_table.id}")
    return db_table


@router.delete("/{table_id}")
def delete_table(table_id: int, session: Session = Depends(get_session)):
    reservations = session.exec(
        select(Reservation).where(Reservation.table_id == table_id)
    ).all()

    if reservations:
        raise HTTPException(status_code=400, detail="Cannot delete table with active reservations")

    table = session.get(Table, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    session.delete(table)
    session.commit()
    return {"ok": True}

