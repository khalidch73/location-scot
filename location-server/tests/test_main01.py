from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 07 Test for creating a location
def test_create_location():
    # Define the request body
    location_data = {"name": "Test_Location_002", "location": "Test City"}

    # Send a POST request to the /locations/ endpoint
    response = client.post("/locations/", json=location_data)

    # Check if the response status code is 200 (indicating success)
    assert response.status_code == 200

    # Check if the response JSON matches the expected structure
    assert "name" in response.json()
    assert "location" in response.json()
    assert response.json()["name"] == location_data["name"]
    assert response.json()["location"] == location_data["location"]

# 08 Test for deleting all locations
def test_delete_all_locations():
    # Send a DELETE request to the /locations/ endpoint
    response = client.delete("/locations/")

    # Check if the response status code is 200 (indicating success)
    assert response.status_code == 200

    # Check if the response contains the expected message indicating successful deletion
    assert response.json() == {"message": "All locations deleted successfully"}