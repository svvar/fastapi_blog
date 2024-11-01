from fastapi import status


def test_correct(client, fill_db):
    response = client.get("comments/daily-breakdown?date_from=2024-10-01&date_to=2024-10-31")

    expected_response = {'summary': {'total_comments': 17, 'blocked_comments': 5},
                         'daily_breakdown': {'2024-10-01': {'total_comments': 3, 'blocked_comments': 1},
                                             '2024-10-02': {'total_comments': 3, 'blocked_comments': 1},
                                             '2024-10-03': {'total_comments': 2, 'blocked_comments': 0},
                                             '2024-10-04': {'total_comments': 1, 'blocked_comments': 1},
                                             '2024-10-05': {'total_comments': 1, 'blocked_comments': 0},
                                             '2024-10-06': {'total_comments': 3, 'blocked_comments': 1},
                                             '2024-10-07': {'total_comments': 2, 'blocked_comments': 0},
                                             '2024-10-08': {'total_comments': 1, 'blocked_comments': 0},
                                             '2024-10-09': {'total_comments': 1, 'blocked_comments': 1}}}

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


def test_no_comments(client, fill_db):
    response = client.get("/comments/daily-breakdown?date_from=2023-01-01&date_to=2023-01-31")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == {'daily_breakdown': {}, 'summary': {'blocked_comments': 0, 'total_comments': 0}}


def test_incorrect_date_format(client, fill_db):
    response = client.get("comments/daily-breakdown?date_from=2024-10-01&date_to=2024.10.31")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = response.json().get("detail")[0]
    assert detail.get("msg") == "Input should be a valid date or datetime, invalid date separator, expected `-`"


def test_incorrect_date_range(client, fill_db):
    response = client.get("comments/daily-breakdown?date_from=2024-10-31&date_to=2024-10-01")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get("detail") == "date_from must be before date_to"


def test_missing_date_from(client, fill_db):
    response = client.get("comments/daily-breakdown?date_to=2024-10-31")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = response.json().get("detail")[0]
    assert detail.get("msg") == "Field required"


def test_missing_dates(client, fill_db):
    response = client.get("comments/daily-breakdown")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = response.json().get("detail")
    assert detail[0].get("msg") == "Field required"
    assert detail[1].get("msg") == "Field required"


def test_incorrect_date(client, fill_db):
    response = client.get("comments/daily-breakdown?date_from=2024-10-01&date_to=2024-10-40")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = response.json().get("detail")[0]
    assert detail.get("msg") == "Input should be a valid date or datetime, day value is outside expected range"

