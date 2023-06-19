from datetime import date

from fastapi import APIRouter, Request, Depends, status
from pydantic import parse_obj_as

from app.booking.dao import BookingDAO
from app.booking.schemas import SBooking
from app.users.models import Users
from app.users.dependecies import get_current_user
from app.exeptions import RoomCannotBeBooked
from app.tasks.tasks import send_email

router = APIRouter(
    prefix="/bookings",
    tags=["Booking"],
)


@router.post("/create")
async def create_booking(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = parse_obj_as(SBooking, booking).dict()
    send_email.delay(booking_dict, user.email)
    return booking_dict


@router.get('')
async def get_user_book(user: Users = Depends(get_current_user)) -> list[SBooking]:
    book = await BookingDAO.find_all(user.id)
    return book


@router.delete('/{booking_id}' )
async def delete_book(booking_id: int, user: Users = Depends(get_current_user)):
    book = await BookingDAO.delete(user_id=user.id, id=booking_id)
    if not book:
        return {'Status': status.HTTP_401_UNAUTHORIZED}
    else:
        return {'Status': status.HTTP_200_OK}
