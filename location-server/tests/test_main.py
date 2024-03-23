# Import necessary modules and classes
from fastapi.testclient import TestClient
from app.main import app

# 01 Define the test client
client = TestClient(app)

# 01 Test for the root route
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Welcome": "Location Finder"}

# 02 Test for creating a location
def test_create_location():
    # Define the request body
    location_data = {"name": "Test_Location_001", "location": "Test City"}

    # Send a POST request to the /locations/ endpoint
    response = client.post("/locations/", json=location_data)

    # Check if the response status code is 200 (indicating success)
    assert response.status_code == 200

    # Check if the response JSON matches the expected structure
    assert "name" in response.json()
    assert "location" in response.json()
    assert response.json()["name"] == location_data["name"]
    assert response.json()["location"] == location_data["location"]

# 03 Test for updating a location by its name
def test_update_location():
    # Define a known location name
    location_name = "Test_Location_001"
    # Define updated location data
    updated_location_data = {"location": "Updated_Location"}

    # Send a PUT request to the /locations/{location_name} endpoint with updated location data
    response = client.put(f"/locations/{location_name}", json=updated_location_data)

    # Check if the response status code is 200 (indicating success)
    assert response.status_code == 200

    # Check if the response contains the expected message indicating successful update
    assert response.json() == {"message": f"Location of '{location_name}' updated successfully"}

# 04 Test for reading a location by its name
def test_read_location():
    # Define a known location name
    location_name = "Test_Location_001"

    # Send a GET request to the /locations/{location_name} endpoint
    response = client.get(f"/locations/{location_name}")

    # Check if the response status code is 200 (indicating success)
    assert response.status_code == 200

    # Check if the response JSON contains the expected location details
    assert "name" in response.json()
    assert "location" in response.json()
    assert response.json()["name"] == location_name

# 05 Test for deleting a location by its name
def test_delete_location():
    # Define a known location name
    location_name = "Test_Location_001"

    # Send a DELETE request to the /locations/{location_name} endpoint
    response = client.delete(f"/locations/{location_name}")

    # Check if the response status code is 200 (indicating success)
    assert response.status_code == 200

    # Check if the response contains the expected message indicating successful deletion
    assert response.json() == {"message": f"Location '{location_name}' deleted successfully"}

# 06 Test for reading all locations
def test_read_all_locations():
    # Send a GET request to the /locations/ endpoint
    response = client.get("/locations/")

    # Check if the response status code is 200 (indicating success)
    assert response.status_code == 200

    # Check if the response contains a list of locations
    assert isinstance(response.json(), list)


