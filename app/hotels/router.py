import asyncio
from datetime import date
from typing import Optional

from fastapi import APIRouter
from fastapi_cache.decorator import cache


from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotels, SHotelInfo


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.get("/{location}")
@cache(expire=30)
async def get_hotels(location: str, date_from: date, date_to: date) -> list[SHotelInfo]:
    await asyncio.sleep(3)
    hotels = await HotelsDAO.find_all(location, date_from, date_to)
    return hotels


@router.get('/id/{hotel_id}')
async def get_hotels_by_id(hotel_id: int) -> Optional[SHotels]:
    return await HotelsDAO.find_one_or_none(id=hotel_id)
