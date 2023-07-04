from datetime import datetime

import pytest

from app.booking.dao import BookingDAO
from app.dao.base import BaseDAO


@pytest.mark.parametrize("user_id, room_id, date_from, date_to", [
    (2, 2, "2023-07-15", "2023-07-30")
])
async def test_add_and_get_booking(user_id, room_id, date_from, date_to):
    date_from = datetime.strptime(date_from, "%Y-%m-%d")
    date_to = datetime.strptime(date_to, "%Y-%m-%d")

    booking = await BookingDAO.add(user_id, room_id, date_from, date_to)

    assert booking
    assert booking.user_id == 2

    new_booking = await BookingDAO.find_by_id(booking.id)

    assert new_booking.id == booking.id
    assert new_booking.user_id == booking.user_id


@pytest.mark.parametrize("user_id, room_id, date_from, date_to", [
    (2, 2, "2023-07-15", "2023-07-30")
])
async def test_delete_get_booking(user_id, room_id, date_from, date_to):
    date_from = datetime.strptime(date_from, "%Y-%m-%d")
    date_to = datetime.strptime(date_to, "%Y-%m-%d")

    add_booking = await BookingDAO.add(user_id, room_id, date_from, date_to)

    assert add_booking
    assert add_booking.user_id == 2

    delete_booking = await BookingDAO.delete(id=add_booking.id)

    user_bookings = await BookingDAO.find_one_or_none(user_id=user_id, id=add_booking.id)

    assert not user_bookings
