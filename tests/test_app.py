import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data
    assert "participants" in data["Soccer Team"]

def test_signup_for_activity_success():
    # Use a unique email to avoid duplicate error
    email = "testuser1@mergington.edu"
    response = client.post(f"/activities/Soccer%20Team/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for Soccer Team" in response.json().get("message", "")
    # Clean up: remove the test user
    data = client.get("/activities").json()
    data["Soccer Team"]["participants"].remove(email)

def test_signup_for_activity_duplicate():
    email = "lucas@mergington.edu"  # Already in Soccer Team
    response = client.post(f"/activities/Soccer%20Team/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")

def test_signup_for_nonexistent_activity():
    email = "testuser2@mergington.edu"
    response = client.post(f"/activities/Nonexistent/signup?email={email}")
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")
