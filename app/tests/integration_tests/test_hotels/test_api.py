import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('date_from, date_to, location, status_code', [
    ('2030-05-01', '2029-05-30', 'Республика Алтай', 400),
    ('2029-05-01', '2029-05-30', 'Республика Алтай', 200),
    ('2029-05-01', '2029-05-30', 'Лагуна Бикини', 200),

])
async def test_get_hotels(date_from, date_to, location, status_code, ac: AsyncClient):
    response = await ac.get(f'hotels/{location}', params={
        'date_from': date_from,
        'date_to': date_to
    })

    if response:
        assert response.status_code == status_code
    else:
        assert response == []


