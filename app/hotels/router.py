from datetime import date
from typing import Optional

from fastapi import APIRouter

from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotels


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.get("/{location}")
async def get_hotels(location: str, date_from: date, date_to: date):
    return await HotelsDAO.find_all(location, date_from, date_to)


@router.get('/id/{hotel_id}')
async def get_hotels_by_id(hotel_id: int) -> Optional[SHotels]:
    return await HotelsDAO.find_one_or_none(id=hotel_id)
