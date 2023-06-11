from datetime import date

from sqlalchemy import select, and_, or_, insert, func

from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.booking.models import Bookings
from app.hotels.schemas import SHotels
from app.dao.base import BaseDAO


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(cls, location: str, date_from: date, date_to: date) -> list[SHotels]:
        """
        СОЗДАЕМ ХРАНИЛИШЕ В КОТОРОЙ ID КОМНАТЫ СОПАСТАВЛЕНА С ТЕМ , СКОЛЬКО РАЗ ЕЕ БРОНИРОВАЛИ!

        with booked_rooms as (
            select room_id, count(room_id) as room_booked
            from booking
            where
                (date_from <= '2023-05-15' and date_from >= '2023-05-30' ) or
                (date_from >= '2023-05-15' and date_to > '2023-05-15')
            group by room_id
        )
        :param location:
        :param date_from:
        :param date_to:
        :return:
        """
        booked_rooms = (
            select(
                Bookings.room_id, func.count(Bookings.room_id).label(
                    "room_booked"
                )
            )
            .select_from(Bookings)
            .where(
                or_(
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_from >= date_to
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to >= date_from
                    )
                )
            )
            .group_by(Bookings.room_id)
            .cte('booked_rooms')
        )
        """
        СОПАСТОВЛЯЕМ ID ОТЕЛЯ СКОЛЬКО КОМНАТ В НЕЙ ОСТАЛОСЬ ЗА ВЫЧЕТОМ УЖЕ ЗАБРОНИРОВАНЫХ 
        
        booked_hotels as(
            select hotel_id, sum(rooms.quantity - coalesce(room_booked, 0)) as rooms_left
            from rooms
            left join booked_rooms on booked_rooms.room_id = rooms.id
            group by hotel_id
        )   
        """
        booked_hotels = (
            select(Rooms.hotel_id, func.sum(
                    Rooms.quantity - func.coalesce(booked_rooms.c.room_booked, 0)
            ).label('rooms_left'))
            .select_from(Rooms)
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .group_by(Rooms.hotel_id)
            .cte('booked_hotels')
        )
        """
        НАХОДИМ НУЖНЫЕ ОТЕЛИ ПО ПАРАМЕТРУ LOCATION , ПРОВЕРЯЕМ ЕСТЬ ЛИ СВОБОДНЫЕ КОМНАТЫ , И 
        ЕСЛИ ЕСТЬ , ТО ОТДАЕМ
        
        select * from hotels
        left join booked_hotels on booked_hotels.hotel_id = hotels.id 
        where rooms_left > 0 and location like "%Алтай%
        """
        get_hotels_with_rooms = (
            select(
                Hotels.__table__.columns,
                booked_hotels.c.rooms_left,
            )
            .join(booked_hotels, booked_hotels.c.hotel_id == Hotels.id, isouter=True)
            .where(
                and_(
                    booked_hotels.c.rooms_left > 0,
                    Hotels.location.like(f"%{location}%")
                )
            )
        )
        async with async_session_maker() as session:
            hotels_with_rooms = await session.execute(get_hotels_with_rooms)
            return hotels_with_rooms.mappings().all()
