from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from sqlmodel import Session, select, and_
from app.db import get_session
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate
from typing import List
import logging

# Настройка логгирования
logger = logging.getLogger(__name__)

router = APIRouter()


def is_time_slot_available(session: Session, table_id: int, start_time: datetime, duration_minutes: int) -> bool:
    """Проверка доступности времени для бронирования."""
    end_time = start_time + timedelta(minutes=duration_minutes)

    # Получаем все бронирования для стола
    reservations = session.exec(
        select(Reservation).where(
            Reservation.table_id == table_id
        )
    ).all()

    # Проверяем пересечения вручную
    for reservation in reservations:
        reservation_end_time = reservation.reservation_time + timedelta(minutes=reservation.duration_minutes)
        if reservation.reservation_time < end_time and reservation_end_time > start_time:
            return False

    return True


@router.get("/", response_model=List[Reservation])
def get_reservations(session: Session = Depends(get_session)):
    logger.info("Fetching all reservations.")
    reservations = session.exec(select(Reservation)).all()
    logger.info(f"Found {len(reservations)} reservations.")
    return reservations


@router.post("/", response_model=Reservation)
def create_reservation(reservation: ReservationCreate, session: Session = Depends(get_session)):
    logger.info(f"Creating reservation for {reservation.customer_name} at table {reservation.table_id}.")

    start_time = reservation.reservation_time
    duration_minutes = reservation.duration_minutes
    end_time = start_time + timedelta(minutes=duration_minutes)

    if not is_time_slot_available(session, reservation.table_id, start_time, duration_minutes):
        logger.warning(
            f"Reservation conflict detected for table {reservation.table_id} during {start_time} - {end_time}")
        raise HTTPException(status_code=400, detail="Table is already reserved at this time.")

    db_reservation = Reservation(**reservation.model_dump())
    session.add(db_reservation)
    session.commit()
    session.refresh(db_reservation)
    logger.info(f"Reservation created for {reservation.customer_name} at table {reservation.table_id}.")
    return db_reservation


@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, session: Session = Depends(get_session)):
    logger.info(f"Attempting to delete reservation with ID: {reservation_id}")
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        logger.warning(f"Reservation with ID {reservation_id} not found.")
        raise HTTPException(status_code=404, detail="Reservation not found")
    session.delete(reservation)
    session.commit()
    logger.info(f"Reservation with ID {reservation_id} deleted.")
    return {"ok": True}
