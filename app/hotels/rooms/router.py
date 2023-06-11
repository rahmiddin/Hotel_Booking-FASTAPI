from datetime import date
from typing import List

from app.hotels.rooms.dao import RoomsDAO
from app.hotels.router import router
from app.hotels.rooms.schemas import SRoomInfo


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_time(hotel_id: int, date_from: date, date_to: date) -> List[SRoomInfo]:
    rooms = await RoomsDAO.find_all(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    return rooms
