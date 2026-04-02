import copy

import src.app as app_module
from fastapi.testclient import TestClient

client = TestClient(app_module.app)
INITIAL_ACTIVITIES = copy.deepcopy(app_module.activities)


def reset_activities():
    app_module.activities = copy.deepcopy(INITIAL_ACTIVITIES)


def test_get_activities_returns_activities():
    # Arrange
    reset_activities()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_success():
    # Arrange
    reset_activities()
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_duplicate_returns_400():
    # Arrange
    reset_activities()
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"
    response_first = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response_first.status_code == 200

    # Act
    response_second = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response_second.status_code == 400
    assert "already signed up" in response_second.json()["detail"]


def test_remove_participant_success():
    # Arrange
    reset_activities()
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    assert email in app_module.activities[activity_name]["participants"]

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]


def test_remove_nonexistent_participant_returns_404():
    # Arrange
    reset_activities()
    activity_name = "Chess Club"
    email = "missing@mergington.edu"
    assert email not in app_module.activities[activity_name]["participants"]

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert "is not registered" in response.json()["detail"]
