from urllib.parse import quote

import pytest

import src.app as app_module


@pytest.mark.xfail(reason="Capacity enforcement is not implemented yet", strict=False)
def test_signup_rejects_when_activity_is_full(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")
    activity = app_module.activities[activity_name]
    seats_to_fill = activity["max_participants"] - len(activity["participants"])

    for index in range(seats_to_fill):
        email = f"capacity-fill-{index}@mergington.edu"
        client.post(f"/activities/{encoded_activity}/signup", params={"email": email})

    # Act
    overflow_response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": "overflow.student@mergington.edu"},
    )

    # Assert
    assert overflow_response.status_code == 400


@pytest.mark.xfail(reason="Email validation is not implemented yet", strict=False)
def test_signup_rejects_blank_email(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(f"/activities/{encoded_activity}/signup", params={"email": "   "})

    # Assert
    assert response.status_code == 400


@pytest.mark.xfail(reason="Email normalization is not implemented yet", strict=False)
def test_signup_rejects_case_insensitive_duplicate_email(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")
    existing_email_different_case = "MICHAEL@MERGINGTON.EDU"

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": existing_email_different_case},
    )

    # Assert
    assert response.status_code == 400