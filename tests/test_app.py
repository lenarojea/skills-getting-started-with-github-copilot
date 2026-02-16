from fastapi.testclient import TestClient
from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Should return a dict of activities
    assert isinstance(data, dict)
    # Known activity present
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity_name = "Chess Club"
    email = "test.user@example.com"

    # Ensure not already present
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    # Signup
    signup_resp = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert signup_resp.status_code == 200
    assert any(email == p for p in activities[activity_name]["participants"])

    # Duplicate signup should fail
    dup_resp = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert dup_resp.status_code == 400

    # Unregister
    unregister_resp = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    assert unregister_resp.status_code == 200
    assert email not in activities[activity_name]["participants"]
