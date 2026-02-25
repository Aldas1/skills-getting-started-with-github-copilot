from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app, follow_redirects=False)


def test_get_root():
    """
    Test GET / endpoint redirects to /static/index.html
    AAA Pattern:
    - Arrange: TestClient is ready
    - Act: Make GET request to root
    - Assert: Verify redirect status and location
    """
    # Arrange
    # (setup is implicit - client is ready)

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities():
    """
    Test GET /activities returns all activities with correct structure
    AAA Pattern:
    - Arrange: TestClient is ready
    - Act: Make GET request to /activities
    - Assert: Verify response contains expected activities
    """
    # Arrange
    # (setup is implicit - client is ready)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Basketball Team" in data
    assert "Programming Class" in data
    # Verify structure of activity object
    assert "description" in data["Chess Club"]
    assert "schedule" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]
    assert "participants" in data["Chess Club"]


def test_signup_success():
    """
    Test successful signup for an activity
    AAA Pattern:
    - Arrange: Prepare email for new student
    - Act: Make POST request to signup endpoint
    - Assert: Verify success response with confirmation message
    """
    # Arrange
    email = "newstudent@example.com"
    activity_name = "Chess Club"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_invalid_activity():
    """
    Test signup fails with 404 when activity doesn't exist
    AAA Pattern:
    - Arrange: Prepare request with nonexistent activity
    - Act: Make POST request to signup endpoint
    - Assert: Verify 404 error response
    """
    # Arrange
    email = "student@example.com"
    invalid_activity = "Nonexistent Activity"

    # Act
    response = client.post(
        f"/activities/{invalid_activity}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_duplicate():
    """
    Test signup fails with 400 when student already signed up
    AAA Pattern:
    - Arrange: Sign up a student first
    - Act: Try to sign up the same student again
    - Assert: Verify 400 error response
    """
    # Arrange
    email = "duplicate@example.com"
    activity_name = "Programming Class"
    # First signup
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()
