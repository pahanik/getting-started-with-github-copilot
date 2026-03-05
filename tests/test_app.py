


import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_unregister_from_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    test_email = "someone@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": test_email})
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"

def test_unregister_from_activity_not_registered():
    # Arrange
    activity = "Chess Club"
    test_email = "notregistered@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": test_email})
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student not registered for this activity"

def test_unregister_from_activity_success():
    # Arrange
    activity = "Chess Club"
    test_email = "removeuser@mergington.edu"
    # First, sign up the user
    client.post(f"/activities/{activity}/signup", params={"email": test_email})
    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": test_email})
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Removed {test_email} from {activity}"

def test_list_activities():
    # Arrange
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_signup_for_activity_success():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Signed up {test_email} for {activity}"


def test_signup_for_activity_already_signed_up():
    # Arrange
    test_email = "michael@mergington.edu"  # Already signed up for Chess Club
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_not_found():
    # Arrange
    test_email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_for_activity_full():
    # Arrange
    activity = "Tennis Club"  # max_participants = 10, already has 1
    # Fill up the activity
    emails = [f"fulluser{i}@mergington.edu" for i in range(2, 12)]
    for email in emails:
        client.post(f"/activities/{activity}/signup", params={"email": email})
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": "overflow@mergington.edu"})
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Activity is full"
